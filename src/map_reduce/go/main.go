package main

import (
	"bufio"
	"flag"
	"fmt"
	"log"
	"os"
	"runtime"
	"runtime/pprof"
	"strconv"
	"strings"
	"sync"
	"time"
)

const CHUNK_SIZE int = 1000000 // lines in chunk
var cpuprofile = flag.String("cpuprofile", "cpu.prof", "write cpu profile to `file`")
var memprofile = flag.String("memprofile", "memory.prof", "write memory profile to `file`")

func mergeMaps(first map[string]int, second map[string]int) {
	merged := first
	for key := range second {
		if _, ok := second[key]; ok {
			merged[key] = merged[key] + second[key]
		} else {
			merged[key] = second[key]
		}
	}
}

func getChunk(fileobj *os.File) <-chan []string {
	// generator
	reader := bufio.NewReader(fileobj)
	channel := make(chan []string)
	cancel_chunk := false
	// Read and return the chunk
	go func() {
		chunk := make([]string, CHUNK_SIZE)
		for {
			for i := 0; i < CHUNK_SIZE; i++ {
				line_bytes, _, err := reader.ReadLine()
				if err != nil {
					if err.Error() == "EOF" {
						cancel_chunk = true
						break
					}
					log.Fatal(err)
				}
				if len(chunk) != 0 {
					chunk[i] = string(line_bytes)
				}
			}
			channel <- chunk
			if cancel_chunk {
				break
			}
		}
		close(channel)
	}()

	return channel
}

func mapFrequencies(chunk []string, wg *sync.WaitGroup, channel *chan map[string]int) <-chan map[string]int {
	defer wg.Done()
	counter := make(map[string]int)
	for _, line := range chunk {
		splited_line := strings.Split(line, "\t")
		if len(splited_line) == 1 {
			continue
		}

		word, count := splited_line[0], splited_line[2]
		count_int, _ := strconv.Atoi(count)
		if _, ok := counter[word]; ok {
			counter[word] = counter[word] + count_int
		} else {
			counter[word] = count_int
		}

	}

	*channel <- counter
	return *channel
}

func main() {
	// for profiling
	flag.Parse()
	if *cpuprofile != "" {
		f, err := os.Create(*cpuprofile)
		if err != nil {
			log.Fatal("could not create CPU profile: ", err)
		}
		defer f.Close() // error handling omitted for example
		if err := pprof.StartCPUProfile(f); err != nil {
			log.Fatal("could not start CPU profile: ", err)
		}
		defer pprof.StopCPUProfile()
	}

	if *memprofile != "" {
		f, err := os.Create(*memprofile)
		if err != nil {
			log.Fatal("could not create memory profile: ", err)
		}
		defer f.Close() // error handling omitted for example
		runtime.GC()    // get up-to-date statistics
		if err := pprof.WriteHeapProfile(f); err != nil {
			log.Fatal("could not write memory profile: ", err)
		}
	}
	//

	startTime := time.Now()
	var wg sync.WaitGroup
	fileobj, err := os.OpenFile("../googlebooks-eng-all-1gram-20120701-a", os.O_RDONLY, 0666)
	if err != nil {
		fmt.Println(err)
		return
	}
	defer fileobj.Close()
	final_result := make(map[string]int)

	for {
		go_results := make(chan map[string]int, runtime.NumCPU()) // not try to change this line
		i := 0
		for chunk := range getChunk(fileobj) {
			i++
			wg.Add(1)
			go mapFrequencies(chunk, &wg, &go_results)
			if i == runtime.NumCPU() {
				break
			}
		}
		wg.Wait()
		val, ok := <-go_results
		if !ok || len(val) == 0 {
			break
		} else {
			go_results <- val //push back value to channel
		}
		close(go_results)
		for result_map := range go_results {
			mergeMaps(final_result, result_map)
		}
	}

	fmt.Printf("Aardvark has appeared %v times.", final_result["Aardvark"])
	fmt.Printf("All time: %d seconds\n", time.Now().Unix()-startTime.Unix())
}

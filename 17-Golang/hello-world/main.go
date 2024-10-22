package main

import "fmt"

func main() {

	sum := 0

	for i := 1; i < 10000000; i++ {
		sum += i
		sum := sum * 2
		fmt.Print(sum)
		fmt.Println(sum)
	}
}

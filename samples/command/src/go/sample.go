// This file is a "Hello, world!" in Go language for wandbox.
package main

import (
	"fmt"

	test1 "./test"
	"./test2"
	"./test3"
)

func main() {
	fmt.Println("Hello, Wandbox!")
	test1.Test()
	test2.Test()
	test3.Test()
}

// Go language references:
//   https://golang.org/pkg/

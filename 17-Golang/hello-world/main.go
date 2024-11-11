package main // 28:14

import "fmt"

func main() {

	// -------------------------------------------------------------------
	// ---------------------- VARIABLE SECTION ---------------------------
	// -------------------------------------------------------------------

	// var _170Byte byte = 170
	// fmt.Println(string(_170Byte))
	// fmt.Println(fmt.Sprintf("%8b", _170Byte))

	// var name string = "John"
	// var family string
	// var age uint8 = 127
	// var isMarried bool = true
	// var hasChildren bool
	// var height byte
	// fmt.Println(name, family, age, isMarried, hasChildren, height)
	// var car = "BMW"

	// fmt.Println(fmt.Sprintf("%T", height)) // return type of variable

	// var (
	// 	name        string = "John"
	// 	family      string
	// 	age         uint8 = 127
	// 	isMarried   bool  = true
	// 	hasChildren bool
	// 	height      byte
	// )

	// const daysOfWeek uint8 = 7

	// -------------------------------------------------------------------
	// ---------------------- FUNCTION SECTION ---------------------------
	// -------------------------------------------------------------------

	// var (
	// 	fullName string
	// 	age      int
	// )
	// fullName, age = fullNameGenerator("masoud", "nazarpoor", 10)

	// var sum = func(a int, b int) int {
	// 	return a + b
	// }

	// -------------------------------------------------------------------
	// ---------------------- ARRAY SECTION ------------------------------
	// -------------------------------------------------------------------

	// var fixedArr = [4]uint16{10, 20, 3, 15}
	// arr := fixedArr[:]
	// arr = append(arr, 1000)

	// for i := range arr {
	// 	memoryAddress := uintptr(unsafe.Pointer(&arr[i]))
	// 	fmt.Printf("%d \n", memoryAddress)
	// }

	// for k, v := range arr {
	// 	// fmt.Printf("%d : %d \n", k, v)
	// 	fmt.Println("index: ", k, " value: ", v)
	// }

	// var users = [10]int64{1, 2, 3, 4}
	// fmt.Println(cap(users), len(users))

	// -------------------------------------------------------------------
	// ---------------------- SLICE SECTION ------------------------------
	// -------------------------------------------------------------------

	var myslice = []int{1, 2, 3}
	fmt.Println(len(myslice), cap(myslice))
	myslice = append(myslice, 4)
	fmt.Println(len(myslice), cap(myslice))
	myslice = append(myslice, 5, 6, 7)
	fmt.Println(len(myslice), cap(myslice))
	myslice = append(myslice, myslice...)
	fmt.Println(len(myslice), cap(myslice))

}

// -------------------------------------------------------------------
// ---------------------- FUNCTION SECTION ---------------------------
// -------------------------------------------------------------------

// func fullNameGenerator(firstName, lastName string, age int) (string, int) {
// 	var fullName string = firstName + " " + lastName
// 	age = age * 2
// 	return fullName, age
// }

// func fullNameGenerator2(firstName, lastName string, age int) (res1 string, res2 int) {
// 	res1 = firstName + " " + lastName
// 	res2 = age * 2
// 	return res1, res2
// }

// func sum(nums ...int) {
// 	fmt.Println(nums)
// }

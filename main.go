package main

import (
	"bufio"
	"flag"
	"fmt"
	"math/rand"
	"os"
	"strconv"
	"strings"
)

type marker byte

const (
	clear  marker = iota
	opaque marker = iota + 10
	bomb
)

func (m marker) String() string {
	switch m {
	case opaque:
		return "."
	case bomb:
		return "B"
	case clear:
		return " "
	case 1, 2, 3, 4, 5, 6, 7, 8, 9:
		return string('0' + m)
	default:
		return "?"
	}
}

type grid [][]marker

type Board struct {
	Shown     grid
	Mines     grid
	Remaining int
}

func (b *Board) Prompt() (bool, int, int) {
	scanner := bufio.NewScanner(os.Stdin)
	for {
		msg := " [%d] (preface with 'b' to mark bomb) cell: "
		fmt.Printf(msg, b.Remaining)
		scanner.Scan()
		reply := strings.TrimSpace(scanner.Text())
		if reply == "" {
			continue
		}
		if strings.EqualFold(reply, "q") {
			os.Exit(0)
		}
		f := strings.Fields(reply)
		if len(f) < 2 {
			fmt.Println("incomplete response!")
			continue
		}
		marked := strings.EqualFold(f[0], "b")
		if marked {
			f = f[1:]
			// ignore anything after second element....
			if len(f) < 2 {
				fmt.Println("incomplete!")
				continue
			}
		}
		x, err := strconv.Atoi(f[0])
		if err != nil {
			fmt.Println("invalid data:", err)
			continue
		}
		y, err := strconv.Atoi(f[1])
		if err != nil {
			fmt.Println("invalid data:", err)
			continue
		}
		// UI has 1-based arrays, but internally we use 0-based
		return marked, x - 1, y - 1
	}
	panic("never here")
}

func (g grid) line() {
	fmt.Println("    " + strings.Repeat("----", len(g)))
}

func (g grid) show() {
	// Header
	fmt.Print("    ")
	for x := range g {
		fmt.Printf(" %2d ", x+1)
	}
	fmt.Println()
	g.line()
	// the matrix
	for y, row := range g {
		fmt.Printf(" %2d |", y+1)
		for _, col := range row {
			fmt.Printf(" %s |", col)
		}
		fmt.Println()
		g.line()
	}
}

func newGrid(size int) grid {
	a := make(grid, size)
	for i := range a {
		a[i] = make([]marker, size)
	}
	return a
}

func populate(size, count int, g grid) grid {
	for count > 0 {
		x := rand.Intn(size)
		y := rand.Intn(size)
		if g[y][x] != bomb {
			g[y][x] = bomb
			count--
		}
	}
	// mark counts for cells neighboring a bomb
	for y := range g {
		for x := range g[y] {
			if count := g.nearby(x, y); count > 0 {
				g[y][x] = marker(count)
			}
		}
	}
	return g
}

// make an fresh 'opaque' board
func wipe(g grid) grid {
	for _, row := range g {
		for x := range row {
			row[x] = opaque
		}
	}
	return g
}

func NewBoard(size, count int) *Board {
	return &Board{
		Mines:     populate(size, count, newGrid(size)),
		Shown:     wipe(newGrid(size)),
		Remaining: count,
	}
}

func (g grid) valid(x, y int) bool {
	return x >= 0 && x < len(g) && y >= 0 && y < len(g)
}

func (g grid) bombCheck(x, y int) int {
	if g.valid(x, y) && (g[y][x] == bomb) {
		return 1
	}
	return 0
}

func (g grid) nearby(x, y int) int {
	// skip if the square is a bomb itself
	if g.bombCheck(x, y) == 1 {
		return 0
	}

	// clockwise evaluation makes it clear all neighbors are checked

	count := 0
	count += g.bombCheck(x, y-1)   // top
	count += g.bombCheck(x+1, y-1) // top-right
	count += g.bombCheck(x+1, y)   // right
	count += g.bombCheck(x+1, y+1) // bottom-right
	count += g.bombCheck(x, y+1)   // bottom
	count += g.bombCheck(x-1, y+1) // bottom-left
	count += g.bombCheck(x-1, y)   // left
	count += g.bombCheck(x-1, y-1) // top-left
	return count
}

func main() {
	size := 10
	count := 5

	flag.IntVar(&size, "size", size, "grid size")
	flag.IntVar(&count, "count", count, "number of mines")
	flag.Parse()

	// make sure input was valid (was passing args w/o flags and ignoring it
	if len(flag.Args()) > 0 {
		fmt.Println("unknown args:", flag.Args())
		os.Exit(1)
	}

	board := NewBoard(size, count)
	for board.Move() {
	}
}

func (b *Board) Move() bool {
	for {
		fmt.Println()
		b.Shown.show()
		marked, x, y := b.Prompt()
		if marked {
			b.Shown[y][x] = bomb
			b.Remaining--
			continue
		}
		if b.Mines[y][x] == bomb {
			b.Mines.show()
			println("kaboom!")
			os.Exit(1)
		}
		b.Sweep(x, y)
	}
	return false
}

// Sweep clears all empty tiles surrounding the selected cel
func (b *Board) Sweep(x, y int) {
	// make sure we haven't wandered off the grid
	if !b.Mines.valid(x, y) {
		return
	}

	// already cleared?
	if b.Shown[y][x] == clear {
		return
	}

	// got a bomb count?
	tile := b.Mines[y][x]
	if int(tile) > 0 {
		b.Shown[y][x] = tile
		return
	}

	// clearing one tile at a time...
	if tile == clear {
		b.Shown[y][x] = tile
	}

	// recursive walk
	b.Sweep(x-1, y) // left
	b.Sweep(x+1, y) // right
	b.Sweep(x, y-1) // up
	b.Sweep(x, y+1) // down
}

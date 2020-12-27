package main

import (
	"os"
	"testing"

	"gocv.io/x/gocv"
)

func TestConnection(t *testing.T) {

}

func TestImageUpload(t *testing.T) {

}

func TestImageFromBytesLoad(t *testing.T) {
	webcam, err := gocv.OpenVideoCapture(0)
	if err != nil {
		panic(err)
	}
	defer webcam.Close()

	img := gocv.NewMat()
	webcam.Read(&img)
	gocv.IMWrite("test.png", img)
	img.Close()

	newMat := gocv.IMRead("test.png", gocv.IMReadAnyColor)
	if newMat.Empty() {
		panic("error occurred while loading an image")
	}
	newMat.Close()

	err = os.Remove("test.png")
	if err != nil {
		panic(err)
	}
}

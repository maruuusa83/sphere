Sphere Server
=============

Stitch photos into sphere using maruuusa83/OpenCV.
Use `omnidirectionalPicture` branch of maruuusa83/opencv if you want to try this repository.

This stitcher will use the AKAZE features as feature detector.

## Build
At first, execute make command to use C++ resources.
```
$ make all
```

## Run as API Server
```
$ python3 app.py
```

## A Sample Code of Stitcher
```
$ ./tests/join_test.sh
```
When the program finishes stitching, a result image of the program will be outputted as stitched.png.  

## SphereImageGenerator classs
### Interface
``` python
class SphereImageGenerator():
  stitch(images)
  imjoin(img1, img2)
```

**stitch(images)**  
This method

 * *images* : Pathes of input pictures
 * *return* : -

**imjoin(img1, img2)**  
This method will join two images to one.  

### argment "images" of stitch
SphereImageGenerater.stitch method needs a adjacencies discripton of images as next:

 * L.1 -> N : The number of pictures  
 * L.2 ~ N+1 -> path\[i\] : Pathes of each picture  
 * L.N+2+2i -> n\[i\] : The number of adjacencies of picture i  
 * L.N+2+2i+1 -> p\[j\] : Indexes of adjacencies of picture i  

Example :  
When a arrangement of pictures is as next,
```
[img1][img2][img3]
[img4][img5][img6]
      [img7]
```
Input Discription Script should be as next:
```
10
./img/img1.png
./img/img2.png
./img/img3.png
./img/img4.png
./img/img5.png
./img/img6.png
./img/img7.png
2
2 4
3
1 3 5
2
2 6
2
1 5
4
2 4 6 7
2
3 5
1
5
```

## Clean Project
```
$ make clean
```


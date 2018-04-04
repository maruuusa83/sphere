/**
 * @file PyStitch.hpp
 * @author Daichi Teruya
 */
#include <Python.h>
#include <iostream>
#include <vector>
#include <opencv2/core/core.hpp>
#include <opencv2/imgcodecs/imgcodecs.hpp>
#include <opencv2/stitching.hpp>
#include "./utility.hpp"

#define ___DEBUG_CPP___

//// Definitions of structure ////
// typedef struct _imgsinfo
// {
//     std::vector<std::string> filenames;
// } IMGSINFO;

//// Prototype ////
PyMODINIT_FUNC PyInit_PyStitcher(void);
static PyObject *PyStitcher_stitch(PyObject *self, PyObject *args);

//// Definitions of module ////
static PyMethodDef py_stitcher_methods[] = {
    {"stitch", PyStitcher_stitch, METH_VARARGS, "execute stitcheing of images"},
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef py_stitcher_module = {
    PyModuleDef_HEAD_INIT,
    "PyStitcher", //< name of module
    NULL,
    -1,           //< size of per-interpreter state of the module,
                  //< or -1 if the module keeps state in global variables.
    py_stitcher_methods
};


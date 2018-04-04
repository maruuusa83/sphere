/**
 * @file PyStitch.cpp
 * @brief OpenCVをC++から操作するためのプログラム
 * @author Daichi Teruya
 */
#include "./PyStitcher.hpp"

//// Functions ////
/** \fn Modlue Initialize
 *  \brief モジュールの初期化を行います.
 */
PyMODINIT_FUNC PyInit_PyStitcher(void)
{
    PyObject *m;

    m = PyModule_Create(&py_stitcher_module);
    if (m == NULL){
        return (NULL);
    }

    py_stitcher_error = PyErr_NewException("PyStitcher.error", NULL, NULL);
    Py_INCREF(py_stitcher_error);
    PyModule_AddObject(m, "error", py_stitcher_error);

    return (m);
}

/** @fn stitch function
 *  @brief 画像のパスの一覧を与えられると、すべて1枚に結合して返します。
 *  @param self Pythonインタプリタから渡されるself変数
 *  @param args 結合する画像へのパスを空白区切りでつないだ文字列
 *  @return 画像の結合結果へのパス
 */
static PyObject *PyStitcher_stitch(PyObject *self, PyObject *args)
{
    IMGSINFO imgsinfo;
    if (!parse_args(imgsinfo, args)){
        return (NULL);
    }

    std::vector<cv::Mat> imglist;
    if (!read_images(imglist, imgsinfo.filenames)){
        return (NULL);
    }

    cv::Mat result;
    auto stitcher = cv::Stitcher::createWithAkaze(true);
    auto status = stitcher.stitchOmnidirectionalPicture(imglist, imgsinfo.adj, result);
    if (status != cv::Stitcher::OK){
        PyErr_SetString(py_stitcher_error, "Stitcher error");
        return (NULL);
    }

#ifdef ___DEBUG_CPP___
    cv::imwrite("stitched.png", result);
#endif
    
    // Python側にNoneを返すための構文
    // NULLを返すとエラーだと思われるので、Noneを表すオブジェクトを返す。
    Py_INCREF(Py_None);
    return (Py_None);
}


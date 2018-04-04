#ifndef ___UTILITY_HPP___
#define ___UTILITY_HPP___

#include <string>
#include <vector>
#include <sstream>
#include <iterator>

//// Constants ////
const char DELIMITER_PURSE_ARGS = ' ';

//// Global Valiables ////
static PyObject *py_stitcher_error; //< the container of error objects
static bool py_stitcher_error_flag = false; //< the container of error objects

//// Definitions of structure ////
typedef struct _imgsinfo
{
    std::vector<std::string> filenames;
    std::vector< std::vector<int> > adj;
} IMGSINFO;

/** @fn read images
 *  @brief 画像群を読み込みます
 */
bool read_images(std::vector<cv::Mat> &result, const std::vector<std::string> &filenames)
{
    for (auto &filename : filenames){
        auto img = cv::imread(filename);
        if (img.empty()){
            PyErr_SetString(py_stitcher_error, "Image file not found");
            py_stitcher_error_flag = true;
            return (false);
        }

        result.push_back(img);
    }

    return (true);
}

/** @fn parse args
 *  @brief Pythonから渡される文字列のパーサです
 *  @param result 結果を保存します
 *  @param args パースする引数です。PyArg_ParseTupleの影響でconstが付けられませんが、変更は加えられません。
 */
bool parse_args(IMGSINFO &result, PyObject *args)
{
    const char *c_str;

    // PyObjectのパース
    if (!PyArg_ParseTuple(args, "s", &c_str)){
        PyErr_SetString(py_stitcher_error, "PyObject-argments Error");
        py_stitcher_error_flag = true;
        return (false);
    }
    std::string str(c_str);

    // 文字列の分割
    // ホワイトスペース区切りで分割します
    std::istringstream iss(str);
    std::vector<std::string> parsed_str;
    copy(std::istream_iterator<std::string>(iss), std::istream_iterator<std::string>(), std::back_inserter(parsed_str));

    // 入力の解析
    // 入力を解析してIMGSINFOに保存していきます
    int num_image = std::stoi(parsed_str[0]);
    printf("num_image = %d\n", num_image);

    int base_pos = 1;
    for (int i = 0; i < num_image; i++){
        result.filenames.push_back(parsed_str[base_pos + i]);
    }
    base_pos += num_image;

    for (int i = 0; i < num_image; i++){
        int num_adj = std::stoi(parsed_str[base_pos]);
        base_pos++;

        std::vector<int> adj_lst;
        for (int j = 0; j < num_adj; j++){
            adj_lst.push_back(std::stoi(parsed_str[base_pos + j]) - 1);
        }
        result.adj.push_back(adj_lst);
        base_pos += num_adj;
    }

#ifdef ___DEBUG_CPP___
    std::cout << "--- IMG PATHES LIST ---" << std::endl;
    for (auto filename : result.filenames){
        std::cout << "  " << filename << std::endl;
    }

    for (auto adj_info : result.adj){
        for (auto adj_num : adj_info){
            std::cout << adj_num << " ";
        }
        std::cout << std::endl;
    }
    std::cout << "-----------------------" << std::endl;
#endif

    return (true);
}
 
#endif /* ___UTILITY_HPP___ */

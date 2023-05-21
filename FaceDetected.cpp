#include <opencv2/opencv.hpp>
#include <iostream>
#include <cstdlib>

using namespace cv;
using namespace std;

static const String model = "res10_300x300_ssd_iter_140000_fp16.caffemodel";
static const String config = "deploy.prototxt";

void detect_dnn_face1() {
    cv::String command;
    VideoCapture capture(-1, cv::CAP_V4L2);
    if(!capture.isOpened()) {
        cerr << "A Camera is not opened" << endl;
        return;
    }
    dnn::Net net = dnn::readNet(model, config);
    if (net.empty()) {
        cerr << "The Net open is failed." << std::endl;
        return;
    }

    Mat frame;
    namedWindow("FRAME");
    
    float confidenceThreshold = 0.9; // 실행할 조건의 임계값 설정

    while(true)
    {
        capture >> frame;
        Mat blob = dnn::blobFromImage(frame, 1, Size(300, 300), Scalar(104, 177, 123));
        net.setInput(blob); //  입력
        Mat result = net.forward();
        Mat detect(result.size[2], result.size[3], CV_32FC1, result.ptr<float>());

        
        for (int i = 0; i < detect.rows; ++i)
        {
            float CONFIDENCE = detect.at<float>(i, 2);  //column 2가 정확도
            if (CONFIDENCE < confidenceThreshold)
                continue; 
            if (CONFIDENCE >= confidenceThreshold) 
            {
                cv::waitKey(5000);
                command = "./2 127.0.0.1 9999"; // 실행할 명령어
                std::system(command.c_str());
                std::cout << "서버 연결" << std::endl;
                std::cout <<  CONFIDENCE << std::endl;
            }
            int x1 = cvRound(detect.at<float>(i, 3) * frame.cols);
            int y1 = cvRound(detect.at<float>(i, 4) * frame.rows);
            int x2 = cvRound(detect.at<float>(i, 5) * frame.cols);
            int y2 = cvRound(detect.at<float>(i, 6) * frame.rows);
        
            rectangle(frame, Rect(Point(x1, y1), Point(x2, y2)), Scalar(0, 255, 0));

            String label = format("Face : %5.3f", CONFIDENCE);
            putText(frame, label, Point(x1, y1 - 1), FONT_HERSHEY_COMPLEX, 0.8, Scalar(0, 255, 0));

            

        }

        imshow("FRAME", frame);
        if(waitKey(10) == 27) break;
    }
        destroyAllWindows();
}





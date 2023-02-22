# Hướng dẫn cài đặt và huấn luyện các model ASR trên toolkit ESPnet

## Các paper cần đọc

[Attention Is All You Need](https://arxiv.org/pdf/1706.03762.pdf)

[Conformer: Convolution-augmented Transformer for Speech Recognition](https://arxiv.org/pdf/2005.08100.pdf)

## ESPnet

Paper: [ESPnet: End-to-End Speech Processing Toolkit](https://arxiv.org/pdf/1804.00015.pdf)

Github: <https://github.com/espnet/espnet>

Phiên bản sử dụng: 0.10.2

## Cài đặt

* ESPnet đang có hai phiên bản, ESPnet1 và ESPnet2. Khuyến khích sử dụng ESPnetv2 vì ESPnet1 sẽ sớm không còn được cộng đồng support nữa.

* Làm theo hướng dẫn ở [đây](https://espnet.github.io/espnet/installation.html) để cài đặt ESPnet. Nếu sử dụng ESPnet2 thì có thể bỏ qua bước cài đặt Kaldi. Nếu cài đặt trên máy ảo Google Colab và gặp các lỗi về đường dẫn CUDA thì chạy các dòng lệnh dưới đây trong cell:

``` sh
!CUDAROOT=/path/to/cuda

!export PATH=$CUDAROOT/bin:$PATH
!export LD_LIBRARY_PATH=$CUDAROOT/lib64:$LD_LIBRARY_PATH
!export CFLAGS="-I$CUDAROOT/include $CFLAGS"
!export CPATH=$CUDAROOT/include:$CPATH
```

## Huấn luyện các mô hình ASR

Với ESPnet ta cần chú ý chủ yếu đến hai folder ```egs2/``` và ```espnet2/```:  
  
* Folder ```egs2/``` chứa các dataset đã có sẵn trong ESPnet, họ đã viết các script để tiền xử lý các dataset này, cũng như một vài các file config tham khảo để xây dựng các mô hình ASR.

* Folder ```espnet2/``` chứa các code định nghĩa các mô hình deep learning của họ.

Hiện tại, ta sẽ dùng dataset tiếng Việt VIVOS (```egs2/vivos/```).

Folder ```egs2/vivos/asr1/conf/``` chứa các file config mô hình khác nhau để chúng ta tham khảo. File ```egs2/vivos/asr1/run.sh``` thường sẽ được chạy để bắt đầu các bước tải, tiền xử lý dữ liệu, train và test mô hình. Đọc kỹ các tài liệu của ESPnet để hiểu cách toolkit này hoạt động.

Sau này nếu muốn thực nghiệm trên dataset khác, hãy tham khảo các script xử lý của họ trong ```egs2/```

## Mô hình ASR BKTraffic đang sử dụng

Model: Transformer Encoder kết hợp Conformer Decoder

Config file: (link)

## Dataset

VIVOS: [Webpage](https://ailab.hcmus.edu.vn/vivos)

import numpy as np
import cv2


def create_filtered(fname_in, fname_out, fname_kernel, select=1, input_t=1, epsilon=1):

    img = cv2.imread(fname_in)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    img = np.float64(img)
    G_fft2 = np.fft.fft2(img)

    img_out = np.zeros_like(img)
    img_out_fft2 = np.zeros_like(img)
    H = img.shape[0]
    W = img.shape[1]

    img = cv2.imread(fname_kernel)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    img = np.float64(img)

    H = img.shape[0]
    W = img.shape[1]
    img = np.fft.ifftshift(img)
    H_fft2 = np.fft.fft2(img)
    img_out_fft2 = np.array(img_out_fft2, dtype=complex)

    if select == 0:
        # 単純なdeconvolution
        # gauss:3 line:2
        t = complex(10**input_t, 0)
        for v in range(H):
            for u in range(W):
                if abs(H_fft2[v, u]) < t:
                    img_out_fft2[v, u] = G_fft2[v, u] / t
                else:
                    img_out_fft2[v, u] = G_fft2[v, u] / H_fft2[v, u]

    else:
        # wiener
        # gauss:5.5 line:4
        e = complex(10**epsilon, 0)
        for v in range(H):
            for u in range(W):
                kyoyaku = complex(H_fft2[v, u].real, -H_fft2[v, u].imag)
                img_out_fft2[v, u] = (
                    kyoyaku / (H_fft2[v, u] * H_fft2[v, u] + e) * G_fft2[v, u]
                )

    img_out = np.fft.ifft2(img_out_fft2)
    # 値の範囲を[0,255]にする
    img_out = img_out.real
    max = img_out[0][1]
    min = img_out[0][1]
    for v in range(H):
        for u in range(W):
            if u == 0 and v == 0:
                continue
            if img_out[v, u] > max:
                max = img_out[v, u]
            if img_out[v, u] < min:
                min = img_out[v, u]

    for v in range(H):
        for u in range(W):
            img_out[v, u] = (img_out[v, u] - min) / (max - min) * 255

    cv2.imwrite(fname_out, abs(img_out))

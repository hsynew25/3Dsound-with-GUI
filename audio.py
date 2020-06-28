from scipy import *
import scipy.io
import scipy.io.wavfile
import numpy

def Make_3D_Audio(index, audiofilename):

    Filename = "spi3sound_" + str(index) + ".wav"
    Idx_left = []
    Idx_right = []
    temp = []

    HRTF_dic = scipy.io.loadmat('HRTF.mat')     # load hrtf data mat file (large_pinna_frontal)
    HRTF_left = HRTF_dic['left']
    HRTF_right = HRTF_dic['right']

    for i in range(len(HRTF_left)):
        Idx_left.append(HRTF_left[i][index])
        Idx_right.append(HRTF_right[i][index])

    # FFT
    fft_hrtf_L = numpy.fft.fft(Idx_left, 1024)
    fft_hrtf_R = numpy.fft.fft(Idx_right, 1024)

    fs, audiodata = scipy.io.wavfile.read(audiofilename)

    print(len(audiodata))

    Ldata = []
    Rdata = []

    for i in range(len(audiodata)):
        Ldata.append(audiodata[i][0])
        Rdata.append(audiodata[i][1])

    '''
    Windowing
    '''
    Nfrm = 512     # frame length
    double_Nfrm = Nfrm * 2

    windowtime = []
    for i in range(double_Nfrm):
        windowtime.append(i / (double_Nfrm * 2))

    sin_window = []
    for i in range(double_Nfrm):
        sin_window.append(numpy.sin(2 * numpy.pi * windowtime[i]))      # windowtime = [0:1023] / 2048

    '''
    STFT initialization
    '''
    vecprev_left = [0] * double_Nfrm
    vecout_left = []
    vec6_left = [0] * Nfrm
    vec5_left = [0] * double_Nfrm
    vec1_left = [0] * double_Nfrm
    L_result = []

    vecprev_right = [0] * double_Nfrm
    vecout_right = []
    vec6_right = [0] * 512
    vec5_right = [0] * double_Nfrm
    vec1_right = [0] * double_Nfrm
    R_result = []

    '''
    STFT code
    '''
    # LEFT
    for n in range(1, int(len(audiodata) / Nfrm)):
        vec1_left[0:Nfrm] = vec1_left[Nfrm:double_Nfrm]
        vec1_left[Nfrm:double_Nfrm] = Ldata[(n - 1) * Nfrm:n * Nfrm]
        vec2_left = list_mul(vec1_left, sin_window)
        vec3_left = numpy.fft.rfft(vec2_left, double_Nfrm)

        vec3_left = list_mul(vec3_left, fft_hrtf_L)

        vec4_left = numpy.fft.irfft(vec3_left, double_Nfrm)

        vecprev_left = vec5_left
        vec5_left = list_mul(vec4_left, sin_window)

        vec6_left = list_add(vecprev_left[512:1024], vec5_left[0:512])
        vecout_left = vec6_left

        L_result =  L_result + vecout_left

     # RIGHT
        vec1_right[0:Nfrm] = vec1_right[Nfrm:double_Nfrm]
        vec1_right[Nfrm:double_Nfrm] = Ldata[(n - 1) * Nfrm:n * Nfrm]
        vec2_right = list_mul(vec1_right, sin_window)
        vec3_right = numpy.fft.rfft(vec2_right, double_Nfrm)

        vec3_right = list_mul(vec3_right, fft_hrtf_R)

        vec4_right = numpy.fft.irfft(vec3_right, double_Nfrm)

        vecprev_right = vec5_right
        vec5_right = list_mul(vec4_right, sin_window)

        vec6_right = list_add(vecprev_right[512:1024], vec5_right[0:512])
        vecout_right = vec6_right

        R_result = R_result + vecout_right

    '''
    !!!  OUTPUT  !!!
    '''
    Output = numpy.zeros((len(R_result), 2))
    audiodata.setflags(write=1)
    for i in range(len(R_result)):
        audiodata[i][0] = L_result[i]
        audiodata[i][1] = R_result[i]

    scipy.io.wavfile.write(Filename, fs, audiodata)

    '''
    for i in range(99):
    Make_3D_Audio(i,"fin.wav")
    '''


'''
list 끼리 곱하는 함수, 더하는 함수 미리 정의
'''
def list_mul(list1, list2):
    result = []
    for i in range(len(list1)):
        result.append(list1[i] * list2[i])
    return result


def list_add(list1, list2):
    result = []
    for i in range(len(list1)):
        result.append(list1[i] + list2[i])
    return result

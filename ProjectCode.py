import jetson_inference
import jetson_utils
import sys
from select import select

numberlist=[]
imageNet=jetson_inference.imageNet(argv=["--model=resnet18.onnx", "--input_blob=input_0", "--output_blob=output_0", "--labels=labels.txt"])
image=jetson_utils.videoSource("/dev/video0")
while True:
    key=select([sys.stdin],[],[],5)
    if key[0]:
        snapshot=(key[0][0].readline())
        if snapshot=="c\n":
            index, confidence=imageNet.Classify(image.Capture())
            confidence=confidence*100
            label=imageNet.GetClassLabel(index)
            numberlist.append(label)
            print(numberlist)
        if snapshot=="+\n" or snapshot=="-\n" or snapshot=="x\n" or snapshot=="*\n" or snapshot=="/\n":
            left=int(''.join(numberlist))
            numberlist=[]
            operator=snapshot[0]
            print(left)
        if snapshot=="=\n":
            right=int(''.join(numberlist))
            print(right)
            if operator=="+":
                result=left+right
            if operator=="-":
                result=left-right
            if operator=="x" or operator=="*":
                result=left*right
            if operator=="/":
                result=left/right
            print (result)

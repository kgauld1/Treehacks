import sensor, image, time, os, tf

sensor.reset()                         # Reset and initialize the sensor.
sensor.set_pixformat(sensor.GRAYSCALE) # Set pixel format to RGB565 (or GRAYSCALE)
sensor.set_framesize(sensor.QVGA)      # Set frame size to QVGA (320x240)
sensor.set_windowing((240, 240))       # Set 240x240 window.
sensor.skip_frames(time=2000)          # Let the camera adjust.

net = "trained.tflite"
labels = [line.rstrip('\n') for line in open("labels.txt")]

clock = time.clock()
while(True):
    clock.tick()

    img = sensor.snapshot()

    # default settings just do one detection... change them to search the image...
    for obj in tf.classify(net, img, min_scale=1.0, scale_mul=0.8, x_overlap=0.5, y_overlap=0.5):
        #print("**********\nPredictions at [x=%d,y=%d,w=%d,h=%d]" % obj.rect())
        img.draw_rectangle(obj.rect())
        # This combines the labels and confidence values into a list of tuples
        predictions_list = list(zip(labels, obj.output()))

        mconf = 0
        midx = 0
        for i in range(len(predictions_list)):
            confidence = predictions_list[i][1]
            label = predictions_list[i][0]
            if label == 'angry' or label=='sad' or label=='neutral':
                confidence *= 0.9
            if label=='surprised' or label='happy':
                confidence *= 1.1

            if confidence > mconf:
                mconf = max(mconf, confidence)
                midx = i
            #print("%s = %f" % (label, confidence))
            # print("%s = %f" % (label, i))
            #if confidence > 0.9 and label != "unknown":
            #    print("It's a", label, "!")
        print(predictions_list[midx][0])
        #print("%s = %f" % (mlab, mconf))
    #print(clock.fps(), "fps")

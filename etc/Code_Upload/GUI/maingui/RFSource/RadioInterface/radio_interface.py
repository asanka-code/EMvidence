import time


def radio_backend(zmq_source, radio, frequency, sampling_rate):
    """
    Capture data from Gnu Radio backend
    :param zmq_source: The ZMQ Address, full TCP host and port
    :param radio: The radio Hardware to use
    :param frequency: The center Frequency (Hz)
    :param sampling_rate: The sampling rate (Hz)
    :return:
    """
    if radio == "RADIO_HW_DEMO":
        import radio_hw_demo as top_block
    if radio == "RADIO_HW_HACKRF_ONE":
        import radio_hw_hackrf_one as top_block
    print("Creating top_block class...")
    tb = top_block.top_block()
    tb.set_zmq_address = zmq_source
    tb.set_sample_rate(sampling_rate)  # Sample Rate
    tb.set_frequency_0(frequency)  # Center Frequency
    print("Starting top_block...")
    tb.start()
    print("Started...")

    time.sleep(10)
    tb.stop()


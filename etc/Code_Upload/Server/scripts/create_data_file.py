import numpy as np
from sigmf.sigmf_hash import calculate_sha512


def create_sample_recording(data_size:int, datafile_name:str) -> str:
    """
    Create sample recording and retuirn SHA512 hash in hex string
    :param data_size:
    :param datafile_name: Filename to save as
    :return: Hash string
    """
    temp_data = np.arange(data_size, dtype=np.float32)
    temp_data.tofile(datafile_name)
    return calculate_sha512(datafile_name)


output_file = f"sample_recordings/example1.sigmf-data"
file_hash = create_sample_recording(1024, output_file)
print(f"{output_file}: {file_hash}")

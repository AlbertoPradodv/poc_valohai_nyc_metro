import valohai
import pandas as pd

my_data = {
    'myinput': 'datum://0182b0ad-0cee-a0a0-a4f8-ec01b8421bb3'
}
 

valohai.prepare(
    step='preprocess-dataset',
    image='python:3.9',
    default_inputs= my_data
)

#df = pd.read_csv(valohai.inputs("myinput").path())

output_path = valohai.outputs().path(' datum://0182b0ad-0cee-a0a0-a4f8-ec01b8421bb3')

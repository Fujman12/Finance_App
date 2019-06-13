from .core_lbo import LBO_Model

client = LBO_Model('abc')
client.show_output()


## Front page
client.show_entry()
client.show_val_output()
client.show_irr()

## Model
client.show_model()
client.show_bs_output()
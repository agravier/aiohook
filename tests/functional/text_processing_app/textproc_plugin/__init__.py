import textproc_plugin.tokenizer as tokenizer
import textproc_plugin.rudin_shapiro_xor as xor

tokenize = tokenizer.tokenize_in_fixed_chunks
transform = xor.encode

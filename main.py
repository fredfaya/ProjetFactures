from IPython.core.display import HTML
from matplotlib import pyplot as plt
import deepdoctection as dd


analyzer = dd.get_dd_analyzer()  # instantiate the built-in analyzer similar to the Hugging Face space demo

df = analyzer.analyze(path = "../Files/facture1.pdf")  # setting up pipeline
df.reset_state()                 # Trigger some initialization

doc = iter(df)
page = next(doc)



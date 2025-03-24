# RAIMAD in Jupyter Notebook

Although it is discouraged,
you can use RAIMAD in notebook environments
such as Jupyter Notebook, JupyterLab,
and Google Colab.

To install RAIMAD (and any pip package for that matter),
make sure you are using the "terminal"
feature of your notebook environment, rather than a code cell.
Running pip from within code cells may cause a deadlock
in cases where pip wants to ask you a question.

![opening a terminal in Jupyter: file > new > terminal]({{webroot}}img/doc/scrot/jupy_notebook_terminal.png)

After installation, you can use RAIMAD normally.
The `raimad.show()` function can tell that it's running inside
a notebook and will render your component inline with the
code cell's output, rather than opening klayout:

```python exec
import raimad as rai
rai.show(rai.Snowman())
```

You can also download all RAIMAD documentation pages
as `.ipynb` notebook files using the button at the top right of the page.



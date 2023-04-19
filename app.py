#!/usr/bin/env python
# coding: utf-8

# In[ ]:





# In[ ]:


from flask import Flask
app = Flask(__name__)
@app.route("/")
def hello():
    return "Hello, World!"


# In[ ]:


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)


# In[ ]:





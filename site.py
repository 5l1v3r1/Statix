import os
import yaml
from jinja2 import Environment, FileSystemLoader
from css_html_js_minify import html_minify

langs=["tr","en"]
config = yaml.load(open("config.yaml"))

# Capture our current directory
dir = os.path.dirname(os.path.abspath(__file__))

def render_template(template,**kwargs):
    j2_env = Environment(loader=FileSystemLoader(dir), trim_blocks=False)
    return(j2_env.get_template(template).render(kwargs))

def generatePages(lang):
	menu = {}
	for page in config["pages"]:
		if lang in config["pages"][page]["metadata"].keys():
			i=config["pages"][page]["metadata"]["id"]
			if "attribute" in config["pages"][page].keys():
				if config["pages"][page]["attribute"]["hidden"]:
					pass
				else:
					menu[i]=[config["pages"][page]["metadata"][lang]["html"],config["pages"][page]["metadata"][lang]["name"]] 
			else:
				menu[i]=[config["pages"][page]["metadata"][lang]["html"],config["pages"][page]["metadata"][lang]["name"]]

	for page in config["pages"]:
		if lang in config["pages"][page]["metadata"].keys():
			id = config["pages"][page]["metadata"]["id"]
			f=open("output/" + config["pages"][page]["metadata"][lang]["html"],'w')
			if "content" in config["pages"][page].keys():
				content=config["pages"][page]["content"][lang]
				f.write(html_minify(render_template("page."+lang+".html",base=config["pages"][page]["metadata"][lang]["base"],title=config["pages"][page]["metadata"][lang]["name"],menu=menu,content=content,id=id)))
			else:
				f.write(html_minify(render_template("page."+lang+".html",base=config["pages"][page]["metadata"][lang]["base"],title=config["pages"][page]["metadata"][lang]["name"],menu=menu,id=id)))

if __name__ == '__main__':
	
	for lang in langs:
		generatePages(lang)

from sys import argv

START_FILE = "main.php"
DEBUG = "-d" in argv

def get_router(file_404):
    import json as j
    with open("routes.json", "r") as fd:
        data = j.load(fd)
    error_page = data.get("404", file_404)
    error_string = f"""{{?>\n#include "{error_page}"\n<?}}"""
    data[""] = data.get("", data.get("index", data.get("home", "home.php")))
    router_code = []
    for key, item in data.items():
        router_code += [f"""if ($_page == "{key}") {{?>\n#include "{item}"\n<?}} else """]
    router_code += [error_string]
    return f"\n<?php $_page = $_GET['p'] ?? \"\"; {"\n".join(router_code)} ?>"

def preprocess_file(filename):
    print("Preprocessing...")

    import pcpp
    from io import StringIO
    import os

    class Preprocessor(pcpp.Preprocessor):
        def on_file_open(self, is_system_include, includepath):
            if not os.path.exists(includepath):
                return StringIO(f"<p><span style=\"color:red\">internal error:</span> couldn't include '{os.path.basename(includepath)}'</p>")
            
            f = super().on_file_open(is_system_include, includepath)
            content = f.read()
            print("Analizing: ", includepath, "<Routers>" in content)
            modified = content\
                .replace("<define>", "#define") \
                .replace("<Routers>", get_router("404.php")) \
                .replace("<vargs>", "__VA_ARGS__")

            return StringIO(modified)
        
    pp = Preprocessor()

    contents = f"#include \"{filename}\""

    pp.parse(contents)
    pp.line_directive = None

    if DEBUG:
        pp.define("DEBUG 1")
    pp.define("pecho(...) <? echo __VA_ARGS__;?>")
    pp.define("__str__(...) #__VA_ARGS__")
    pp.define("__page__(page) __str__(/labtele?p=page)")
    pp.define("nav(page, element) <div><a href=__page__(page)> element </a></div>")

    output = StringIO()
    pp.write(output)

    print("File preprocessed")

    return output.getvalue()

def save_file(filepath, result):
    print("sending...")
    import paramiko
    import minify_html

    with open("ign.db.pass", "r") as fd:
        dbp = fd.read()

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect("lab.alberghetti.cloud", username="morta.g.181007", password=dbp)

    with open("ign.out.php", "w") as f:
        f.write(result)

    while "\n\n" in result:
        result = result.replace("\n\n", "\n")
    if not DEBUG:
        result = minify_html.minify(result, minify_js=True, minify_css=True)
        result = result.replace(";\n", ";")

    sftp = ssh.open_sftp()
    with sftp.open(filepath, "w") as f:
        f.write(result)
    sftp.close()
    ssh.close()
    print("file sent.")

    with open("ign.out.min.php", "w") as f:
        f.write(result)



def default_styles():
    return """<style>
a { all: unset; }
body { padding: 0; margin: 0; }
.RouterWrapper {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 10px;
    flex: 1;
    padding: 20px;
}
p { margin: 0 }
</style>"""

preprocessed = preprocess_file(START_FILE)
content = "\n".join([default_styles(), preprocessed])
save_file("/var/www/html/labtele/index.php", content)

import site_generation

def main():
    site_generation.copy_files_to_dir("./static", "./public")
    site_generation.generate_page("./content/index.md", "./template.html", "./public/index.html")

if __name__ == "__main__":
    main()
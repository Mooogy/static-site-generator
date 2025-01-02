import site_generation

def main():
    site_generation.copy_files_to_dir("./static", "./public")
    site_generation.generate_pages_recursive("./content", "./template.html", "./public")

if __name__ == "__main__":
    main()
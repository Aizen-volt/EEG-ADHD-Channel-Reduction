from config import DIRECTORIES_TO_CREATE, BASE_DIR, logger


def create_directories():
    for directory in DIRECTORIES_TO_CREATE:
        directory.mkdir(parents=True, exist_ok=True)
        logger.info(f"Dir created (or already existed): {directory.relative_to(BASE_DIR)}")

if __name__ == "__main__":
    create_directories()
    logger.info("Project initialization completed")
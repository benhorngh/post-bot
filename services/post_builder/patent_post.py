from services import data_fetch


def build_post(patent: data_fetch.CPCPatent) -> str:
    return patent.content

import logging
import sys
from pathlib import Path

def get_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    if logger.hasHandlers():
        return logger

    logger.setLevel(logging.INFO)
    
    # Formatação com padrão comum para DataOps (podemos converter pra JSON no futuro)
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    
    # Handler para o Console
    ch = logging.StreamHandler(sys.stdout)
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    
    # Handler para gravação em Arquivo local (root pipeline.log)
    log_file = Path(__file__).parent.parent.parent / "pipeline.log"
    fh = logging.FileHandler(log_file, encoding='utf-8')
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    
    return logger

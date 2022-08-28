import sys
import settings
from bootstrap import bootstrap


if __name__ == "__main__":
    app = bootstrap(settings.get_config())
    app.main(sys.argv[1:])

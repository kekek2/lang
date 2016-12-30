#!/bin/sh

cp ru_RU.po ru_RU.po.old
rm -R /usr/plugins/devel/debug
make src
make template
make merge
./difflang.py > diff.ru_RU.po

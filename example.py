#!/usr/bin/env python3

import shellfish

tpl = shellfish.Template(r"""
          echo "Hello World"
          cat /etc/passwd \
              | grep <(echo {pattern})
          """)
tpl.debug = True
tpl.values = {'pattern': 'man'}
tpl.run()

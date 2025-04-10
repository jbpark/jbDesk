def clear_layout(main_layout):
    while main_layout.count():
        item = main_layout.takeAt(0)
        if item.widget():
            item.widget().setParent(None)
        elif item.layout():
            while item.layout().count():
                sub_item = item.layout().takeAt(0)
                if sub_item.widget():
                    sub_item.widget().setParent(None)

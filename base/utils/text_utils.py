def sanitise_text(node_text=None):
            doc = node_text.document()
            current_text = doc.toPlainText()
            new_text = current_text.replace(" ", "_")
            if new_text != current_text:
                doc.blockSignals(True)
                doc.setPlainText(new_text)
                doc.blockSignals(False)
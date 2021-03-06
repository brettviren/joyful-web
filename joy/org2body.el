(setq org-confirm-babel-evaluate nil)
(setq org-src-fontify-natively t)
(org-babel-do-load-languages
 'org-babel-load-languages
 '(
   (sh . t)
   (python . t)
   (ditaa . t)
   (dot . t)
   (sqlite . t)
   ))

(defun org2body (src tgt)
  "Dump body of org file to HTML"
  (progn
    (save-excursion
      (find-file src)
      (org-html-export-as-html nil nil nil t)
      (with-current-buffer "*Org HTML Export*"
	(write-file tgt)))))


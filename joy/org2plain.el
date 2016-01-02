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

(defun org2plain (src tgt)
  "Dump body of org file to plain text"
  (progn
    (save-excursion
      (find-file src)
      (org-ascii-export-as-ascii)
      (with-current-buffer "*Org ASCII Export*"
	(write-file tgt)))))


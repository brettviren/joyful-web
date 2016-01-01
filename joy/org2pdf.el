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


(defun org2pdf (src tgt)
  "Dump body of org file to HTML"
  (progn
    (save-excursion
      (find-file src)
      (org-latex-export-to-pdf)
      (copy-file
       (concat (file-name-sans-extension src) ".pdf") tgt t)
      )))


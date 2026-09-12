/** Content = index.html only: every class, including those inside JS
 * template strings, is literal text in that one file. `relative: true`
 * resolves the path against this file, not the shell's cwd. */
module.exports = {
  content: { relative: true, files: ['./index.html'] },
  theme: { extend: {} },
  plugins: [],
};

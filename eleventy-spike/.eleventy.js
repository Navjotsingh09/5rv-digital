module.exports = function(eleventyConfig) {
  // Pass static assets through unchanged
  eleventyConfig.addPassthroughCopy("css");
  eleventyConfig.addPassthroughCopy("images");
  eleventyConfig.addPassthroughCopy("js");
  eleventyConfig.addPassthroughCopy("documents");

  return {
    dir: {
      input:    ".",
      includes: "_includes",
      output:   "_site",
    },
    templateFormats: ["njk", "html"],
    htmlTemplateEngine: "njk",
  };
};

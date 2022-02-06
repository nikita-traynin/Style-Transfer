//name the file based on if it was dropped in the content or style dropzones.
//TODO: can this be done on the html layer, to be able to delte this file?

Dropzone.options.contentImageUpload = {
  paramName: "content", // The name that will be used to transfer the file
  maxFilesize: 2, // MB
  acceptedFiles: "image/jpeg"
};

Dropzone.options.styleImageUpload = {
  paramName: "style", // The name that will be used to transfer the file
  maxFilesize: 2, // MB
  acceptedFiles: "image/jpeg"
}

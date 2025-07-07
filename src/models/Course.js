const mongoose = require('mongoose');

const CourseSchema = new mongoose.Schema({
  code: {
    type: String,
    required: true,
    unique: true
  },
  title: {
    type: String,
    required: true
  },
  credits: {
    type: Number,
    required: true
  },
  department: {
    type: String,
    required: true
  }
});

module.exports = mongoose.model('Course', CourseSchema);
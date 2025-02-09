import axios from "axios";
import qs from "qs";

const errorHandling = (error) => {
  if (error.response.status === 403) window.location.replace("/");
};

export const SessionAPI = {
  getSession: () => axios.get(`/api/session`),
  postSession: (userID, password) =>
    axios.post(
      `/api/session`,
      qs.stringify({
        userID,
        password,
      }),
      {
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
        },
      }
    ),
  deleteSession: () => axios.delete(`/api/session`),
};

export const CourseAPI = {
  getCourses: () =>
    axios
      .get(`/api/courses?name&type&description&options&number&students`)
      .catch((error) => errorHandling(error)),
  postCourse: (course) =>
    axios.post(`/api/course`, [course]).catch((error) => errorHandling(error)),
  deleteCourse: (id) =>
    axios
      .delete(`/api/course`, { data: [id] })
      .catch((error) => errorHandling(error)),
  putCourse: (course) =>
    axios.put(`/api/course`, [course]).catch((error) => errorHandling(error)),
  exportCourses: () =>
    axios.get('/api/exportCourses.json').catch((error) => errorHandling(error)),
  importCourses: (courses) =>
    axios.post(`/api/importCourses`, courses).catch((error) => errorHandling(error)),
};

export const StudentDataAPI = {
  getStudentData: () =>
    axios
      .get(`/api/users`, {
        params: {
          name: 1,
          grade: 1,
          authority: 1,
        },
      })
      .catch((error) => errorHandling(error)),
  postStudentData: (users) =>
    axios.post(`/api/users`, users).catch((error) => errorHandling(error)),
  deleteStudentData: (ids) =>
    axios
      .delete(`/api/users`, { data: [...ids] })
      .catch((error) => errorHandling(error)),
  putStudentData: (user) =>
    axios.put(`/api/users`, user).catch((error) => errorHandling(error)),
};

export const PasswordAPI = {
  putPassword: (passwords) =>
    axios
      .put(`/api/password`, passwords)
      .catch((error) => errorHandling(error)),
};

export const SelectAPI = {
  getSelections: (courseID) =>
    axios
      .get(`/api/selections/${courseID}`)
      .catch((error) => errorHandling(error)),
  putSelections: (courseID, data) =>
    axios
      .put(`/api/selections/${courseID}`, [...data])
      .catch((error) => errorHandling(error)), // , [...courseID.data.selected]),
};

const downloadHeader = {
  headers: {
    'Cache-Control': 'no-cache',
    'Pragma': 'no-cache',
    'Expires': '0',
  }
};

export const DistributeAPI = {
  // postDistribute: () => axios.post(`/api/distribute`),
  postDistribute: () => axios.post(`/api/new_distribute`),
  putPreselect: (ids) =>
    axios.put(`/api/preselect`, ids).catch((error) => errorHandling(error)),
  getResult: () => axios.get(`/api/download_result`, downloadHeader),
  getStatistics: () => axios.get(`/api/download_statistics`, downloadHeader),
  resetSelection: () => axios.delete('/api/reset_selection'),
};

export const OpentimeAPI = {
  getOpentime: () => axios.get(`/api/opentime`),
  putOpentime: (start, end) =>
    axios
      .put(`/api/opentime`, { start, end })
      .catch((error) => errorHandling(error)),
};

export const ResultAPI = {
  getResult: () =>
    axios.get("/api/result").catch((error) => errorHandling(error)),
};

export const SampleAPI = {
  getSample: (userID) =>
    axios
      .get("/api/sample", { params: { userID } })
      .catch((error) => errorHandling(error)),
};

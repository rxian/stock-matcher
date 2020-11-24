import axios from 'axios';

const baseURL = process.env.REACT_APP_STAGE === 'development'
    ? "http://157.245.91.247:5000"
    : "http://127.0.0.1:5000";

export default axios.create({
    baseURL: baseURL,
    timeout: 10000,
})

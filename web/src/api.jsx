import axios from 'axios';

export default axios.create({
    // baseURL: "http://127.0.0.1:5000",
    baseURL: "http://157.245.91.247:5000",
    timeout: 10000,
})
import axios from 'axios'
import { Message } from 'element-ui'
// import { Message, MessageBox } from 'element-ui'
import store from '../store'
import { getToken } from '@/utils/auth'
import router from '../router'

// 创建axios实例
const service = axios.create({
  baseURL: process.env.BASE_API, // api 的 base_url
  timeout: 5000 // 请求超时时间
})

// request拦截器
service.interceptors.request.use(
  config => {
    if (store.getters.token) {
      config.headers['Authorization'] = 'JWT ' + getToken()
      // 让每个请求携带自定义token 请根据实际情况自行修改
    }
    return config
  },
  error => {
    // Do something with request error
    console.log(error) // for debug
    Promise.reject(error)
  }
)

// response 拦截器
service.interceptors.response.use(
  response => {
    /**
     * code为非20000是抛错 可结合自己业务进行修改
     */
    // console.log(response)
    return response.data
  },
  error => {
    console.log('err' + error) // for debug,
    // request.js 统一处理异常,每个组件中也可以独立处理异常, 使用.catch(err => {}) 捕获
    if (!error.response) {
      Message.error('系统错误')
    } else if (error.response.status === 401) { // 如果错误是401
      store.dispatch('FedLogOut').then(() => { // 让前端登出
        router.push({ path: '/login' }) // 去登录页面
      })
    } else if (error.response.status === 403) { // 如果没权限
      Message({
        message: '权限拒绝',
        type: 'error',
        duration: 800,
        onClose: function() { // 回调函数onClose
          router.push({ path: '/' }) // 去首页
        }
      })
    } else if (error.response.status === 400) { // 如果是400
      Message({
        message: '认证失败, 用户名或密码错误',
        type: 'error'
      })
    } else if (error.response.status === 500) { // 如果是500
      Message({
        message: '服务内部错误',
        type: 'error'
      })
    }
    return Promise.reject(error)
  }
)

export default service


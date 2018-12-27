import router from './router'
import store from './store'
import NProgress from 'nprogress' // Progress 进度条
import 'nprogress/nprogress.css' // Progress 进度条样式
// import { Message } from 'element-ui'
import { getToken } from '@/utils/auth' // 验权

const whiteList = ['/login'] // 不重定向白名单
router.beforeEach((to, from, next) => {
  NProgress.start()
  if (getToken()) { // 判断是否有key
    if (to.path === '/login') {
      next({ path: '/' }) // 如果有key,要去登陆页面,让去首页
      NProgress.done() // 结束
    } else { // 有了key,去其他任何页面时,获取用户信息
      if (store.getters.name.length === 0) {
        store.dispatch('GetInfo').then(() => { // 拉取用户信息
          next()
        }).catch((err) => {
          console.log(err)
          // store.dispatch('FedLogOut').then(() => {
          //   Message.error(err || 'Verification failed, please login again')
          //   next({ path: '/' })
          // })
        })
      } else {
        next()
      }
    }
  } else { // 如果没有key,看下是否在白名单里,在,就继续
    if (whiteList.indexOf(to.path) !== -1) {
      next()
    } else { // 否则,去登陆页面
      next(`/login?redirect=${to.path}`)
      NProgress.done()
    }
  }
})
router.afterEach(() => {
  NProgress.done() // 结束Progress
})

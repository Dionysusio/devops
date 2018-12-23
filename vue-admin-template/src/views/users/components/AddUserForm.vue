<template>
  <div class="add-user-form">
    <el-dialog :visible.sync="visible" title="创建用户" @close="handleClose">
      <el-form ref="addUserForm" :model="form" :rules="rules" label-width="100px">
        <el-form-item label="登陆名: " prop="username">
          <el-input v-model="form.username" auto-complete="off" placeholder="请输入登陆名" />
        </el-form-item>
        <el-form-item label="姓名: " prop="name">
          <el-input v-model="form.name" placeholder="请输入姓名" />
        </el-form-item>
        <el-form-item label="密码: " prop="password">
          <el-input v-model="form.password" type="password" placeholder="请输入密码" />
        </el-form-item>
        <el-form-item label="手机号: " prop="phone">
          <el-input v-model="form.phone" placeholder="请输入手机号" />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="submitForm">立即创建</el-button>
          <el-button @click="resetForm">重置</el-button>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="handleClose">取 消</el-button>
        <el-button type="primary" @click="handleClose">确 定</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import { addUser } from '@/api/user'
export default {
  name: 'AddUserForm',
  props: {
    value: {
      type: Boolean,
      default: false
    }
  },
  data: function() {
    return {
      visible: false,
      // visible: 决定弹出框是显示还是隐藏
      form: {
        // 弹出框里面的字段
        username: '',
        name: '',
        password: '',
        phone: ''
      },
      rules: {
        username: [
          { required: true, message: '请输入用户名', trigger: 'blur' }
        //  username:验证的字段名, blur:失去光标. 验证的是prop对应的值,和这里的username必须一一对应.
        ],
        name: [
          { required: true, message: '请输入用户姓名', trigger: 'blur' }
        ],
        password: [
          { required: true, message: '请输入密码', trigger: 'blur' }
        ],
        phone: [
          { required: true, message: '请输入联系电话', trigger: 'blur' }
        ]
      }
    }
  },
  watch: {
    value(val) {
      // val 是接收过来的值,props 里的value,如果有值,就等于val,或者等于true
      this.visible = true
    }
  },
  methods: {
    handleClose() {
      // 弹框关闭的时候执行的回调函数
      this.visible = false
      this.$emit('input', false)
      // 触发input事件,传值为false
      this.resetForm()
    },
    resetForm() {
      // 关闭之后重置表单,即重新打开弹窗时,里面是空的
      this.$refs.addUserForm.resetFields()
    },
    submitForm() {
      // 表单提交
      this.$refs.addUserForm.validate((valid) => {
        // 验证
        if (valid) {
          // 如果验证成功,向后台发送创建用户的请求,定义addUser接口
          addUser(this.form).then(() => {
            // 参数this.form 是我们的数据,创建成功,执行then((res) => {}), res是创建成功返回的结果
            // console.log(res)
            this.$message({
              message: `创建用户${this.form.name}成功`,
              type: 'success'
            })
            this.handleClose()
            this.$emit('fetch')
          //  触发fetch事件,刷新数据,即显示创建出来的user. 在父组件监听fetch,定义handleFetch()
          })
        } else {
          console.log('error submit!!')
          return false
        }
      })
    }
  }
}
</script>

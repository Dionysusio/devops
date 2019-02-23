<template>
  <div class="group-form-container">
    <!-- 这个表单功能:添加,修改-->
    <el-dialog :visible.sync="visible" :title="title" @close="handleClose">
      <el-form ref="groupForm" :model="form" :rules="rules" label-width="100px">
        <el-form-item label="用户组：" prop="name">
          <el-input v-model="form.name" placeholder="请输入用户组"/>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="submitForm">提交</el-button>
          <el-button @click="resetForm">重置</el-button>
        </el-form-item>
      </el-form>
    </el-dialog>
  </div>
</template>
<script>
import { addGroup, modifyGroup } from '@/api/group'
export default {
  name: 'GroupForm',
  props: {
    value: {
      type: Boolean,
      default: false
    },
    gid: {
      type: Number,
      default: 0
    },
    gname: {
      type: String,
      default: ''
    }
  },
  data() {
    return {
      visible: false,
      groupId: 0,
      form: {
        name: ''
      },
      rules: {
        name: [
          { required: true, message: '请输入用户组', trigger: 'blur' }
        ]
      }
    }
  },
  computed: {
    title() {
      if (this.groupId === 0) return '创建用户组'
      else return '修改用户组'
    }
  },
  watch: {
    value(val) {
      this.visible = val
    },
    gid(val) {
      if (val < 0) return
      this.groupId = val
    },
    gname(val) {
      if (val === '') return
      this.form.name = val
    }
  },
  methods: {
    resetForm() {
      this.$refs.groupForm.resetFields()
      if (this.groupId === 0) this.form.name = ''
    },
    handleClose() {
      this.visible = false
      this.groupId = 0
      this.resetForm()
      this.$emit('input', false)
    },
    submitForm() { // 提交有2种情况: 添加,修改
      this.$refs.groupForm.validate((valid) => {
        if (valid) {
          this.save()
        } else {
          console.log('error submit!!')
          return false
        }
      })
    },
    save() { // 在这里判断是添加,还是修改. 看有没有id,有的话就是修改,否则就是添加
      if (this.groupId === 0) {
        this.create()
      } else {
        this.update()
      }
    },
    create() {
      addGroup(this.form).then(() => {
        this.$message({
          message: `添加用户组 ${this.form.name} 成功`,
          type: 'success'
        })
        this.handleClose()
        this.$emit('fetch')
      })
    },
    update() {
      modifyGroup(this.groupId, this.form).then(() => {
        this.$message({
          message: `修改用户组 ${this.form.name} 成功`,
          type: 'success'
        })
        this.handleClose()
        this.$emit('fetch')
      })
    }
  }
}
</script>

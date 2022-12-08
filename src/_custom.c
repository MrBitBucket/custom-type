#define PY_SSIZE_T_CLEAN
#include <Python.h>
#define VERSION "0.0.0"

typedef struct {
	PyObject_HEAD
	/* Type-specific fields go here. */
} CustomObject;

static PyTypeObject CustomType = {
	PyVarObject_HEAD_INIT(NULL, 0)
	.tp_name = "_custom.Custom",
	.tp_doc = PyDoc_STR("Custom objects"),
	.tp_basicsize = sizeof(CustomObject),
	.tp_itemsize = 0,
	.tp_flags = Py_TPFLAGS_DEFAULT,
	.tp_new = PyType_GenericNew,
};

static PyModuleDef custommodule = {
	PyModuleDef_HEAD_INIT,
	.m_name = "_custom",
	.m_doc = "Example module that creates an extension type.",
	.m_size = -1,
};

PyMODINIT_FUNC
PyInit__custom(void)
{
	PyObject *m, *v=NULL;
	if (PyType_Ready(&CustomType) < 0)
		return NULL;

	m = PyModule_Create(&custommodule);
	if (m == NULL)
		return NULL;

	Py_INCREF(&CustomType);
	if(PyModule_AddObject(m, "Custom", (PyObject *) &CustomType) < 0) goto err;
	v = PyUnicode_FromString(VERSION);
	if(!v || PyModule_AddObject(m, "version", v)<0) goto err;

	return m;

err:
	Py_XDECREF(v);
	Py_DECREF(&CustomType);
	Py_DECREF(m);
	return NULL;
}

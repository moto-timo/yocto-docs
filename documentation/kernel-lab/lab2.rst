.. SPDX-License-Identifier: CC-BY-SA-2.0-UK

*******************************
Lab2: linux-yocto Kernel Recipe
*******************************

In this lab you will work towards the same end goal as in Lab 1. This
time you will use the `linux-yocto` recipe and tooling. This simplifies
the process of configuring the kernel and makes reusing your work much
easier.

Setup the Environment
=====================

.. code-block:: shell

   $ cd ~/poky/
   $ source oe-init-build-env

Open :file:`local.conf`:

.. code-block:: shell

   $ vi conf/local.conf

Add the following line just above the line that says ``MACHINE ??= “qemux86_64”``:


.. code-block:: shell

   MACHINE ?= "lab2-qemux86"

Save your changes and close :command:`vi`.

Now open :file:`bblayers.conf`:

.. code-block:: shell

   $ vi conf/bblayers.conf

and add the ``'meta-lab2-qemux86'`` layer to the :term:`BBLAYERS`
variable. The final result should look like this, assuming your account is
called 'myacct' (simply copy the line containing 'meta-yocto-bsp'
and replace 'poky/meta-yocto-bsp' with 'kernel-lab-layers/meta-lab2-qemux86'):

.. code-block:: shell

   BBLAYERS ?= " \
     /home/myacct/poky/meta \
     /home/myacct/poky/meta-poky \
     /home/myacct/poky/meta-yocto-bsp \
     /home/myacct/kernel-lab-layers/meta-lab2-qemux86 \
     "

You should not need to make any further changes. Save your changes and
close :command:`vi`.

Review the Lab 2 Layer
======================

This layer differs from ``meta-lab1-qemux86`` only in the Linux kernel
recipes. This layer contains the following files for the kernel:

.. code-block:: shell

   recipes-kernel/
   └── linux
       ├── files
       │   ├── lab2.cfg
       │   ├── mtd-block.cfg
       │   └── yocto-testmod.patch
       ├── linux-yocto_&KERNEL_LAB_LTS_VERSION;.bbappend
       └── linux-yocto_&KERNEL_LAB_STABLE_VERSION;.bbappend

Open the &KERNEL_LAB_STABLE_VERSION; kernel recipe:

.. code-block:: shell

   $ vi ~/kernel-lab-layers/meta-lab2-qemux86/recipes-kernel/linux/linux-yocto_&KERNEL_LAB_STABLE_VERSION;.bbappend

Note that this is not a complete recipe, but rather an extension of
the ``linux-yocto`` recipe provided by the ``poky`` sources. It adds
the layer path for additional files and sets up some machine-specific
variables. Notice that instead of a :file:`defconfig` file, the recipe
adds :file:`lab2.cfg` to the :term:`SRC_URI`. This is a Linux kernel
config fragment. Rather than a complete :file:`.config` file, a config
fragment lists only the config options you specifically want to change.
To start out, this fragment is commented out, and the linux-yocto
sources will provide a default :file:`.config` compatible with common
PC hardware.

The :file:`lab2.cfg` config fragment is an example of a config fragment
that is both defined and specified in 'recipe-space', in other words
defined as a file under the recipe's (in this case) :file:`files/`
directory and added via the :term:`SRC_URI`. Config fragments can also
be defined in the kernel repository's 'meta' branch and added to the
BSP via :term:`KERNEL_FEATURES` statements in the kernel recipe:

.. code-block:: shell

   KBRANCH_lab2-qemux86 = "v&KERNEL_LAB_STABLE_VERSION;/standard/base"
   KMACHINE_lab2-qemux86  = "common-pc"

   KERNEL_FEATURES:append:lab2-qemux86 = " cfg/smp.scc"

In the recipe fragment above, the :file:`cfg/smp.scc` kernel feature,
which maps to the kernel's ``CONFIG_SMP`` configuration setting, is
added to the machine's kernel configuration to turn on SMP capabilities
for the BSP. Kernel features as well as the :term:`KBRANCH` and
:term:`KMACHINE` settings referenced above, which essentially specify
the source branch for the BSP, are all described in detail in
:doc:`/dev-manual/index`.

The ``meta-lab2-qemux86`` machine configuration is very similar to the
``meta-lab1-qemux86`` in Lab 1. Open it in :command:`vi` for review:

.. code-block:: shell

   $ vi ~/kernel-lab-layers/meta-lab2-qemux86/conf/machine/lab2-qemux86.conf

The main difference from the Lab 1 machine configuration is that it
specifies not only a :term:`PREFERRED_PROVIDER` for the
``virtual/kernel`` component, but a :term:`PREFERRED_VERSION` as well:

.. code-block:: shell

   PREFERRED_PROVIDER_virtual/kernel ?= "linux-yocto"
   PREFERRED_VERSION_linux-yocto ?= "&KERNEL_LAB_STABLE_VERSION;%"

Because the Lab 2 layer has multiple kernel implementations available
to it (linux-yocto_&KERNEL_LAB_LTS_VERSION; and
linux-yocto_&KERNEL_LAB_STABLE_VERSION;), there is in this case some
ambiguity about which implementation and version to choose. The above
lines choose a ``linux-yocto`` recipe as the :term:`PREFERRED_PROVIDER`,
and explicitly select the ``linux-yocto_&KERNEL_LAB_STABLE_VERSION;``
version via the :term:`PREFERRED_VERSION` setting (the trailing '%'
serves as a wildcard, meaning in this case to ignore any minor version
in the package version when doing the match).

In this case, the build system would have chosen the same
implementation and version via defaults (``linux-yocto`` by virtue of
the included :file:`qemu.inc`, and ``5.14`` simply because it's the
highest version number available for the ``linux-yocto`` recipes --
this is contained in the logic treating package selection in the build
system), but again, sometimes it makes sense to avoid surprises and
explicitly 'pin down' specific providers and versions.

Build the Image
===============

Now you will build the kernel and assemble it into a qemu bootable
image. This build may take some time, but it will be quicker than
the first build for lab1, since some downloads have already been
accomplished and we benefit from some tasks that have already been
run. This build will need to fetch the kernel source and recompile
for the ``'lab2-qemux86'`` machine.

.. code-block:: shell

   $ bitbake core-image-minimal

.. note::
   For this lab, there will be a number of warning messages of the
   form 'WARNING: Failed to fetch ...'. You can safely ignore those.
   You may also see a warning about the kernel config and the value
   of ``CONFIG_NR_CPUS`` changing. This is also safe to ignore.

Now boot the image with QEMU:

.. code-block:: shell

   $ runqemu nographic tmp/deploy/images/lab2-qemux86/bzImage-lab2-qemux86.bin tmp/deploy/images/lab2-qemux86/core-image-minimal-lab2-qemux86.ext4

Login as root with no password and verify the version of the kernel:

.. code-block:: shell

   root@lab2-qemux86:~# uname -r
   &KERNEL_LAB_STABLE_FULL_VERSION;-yocto-standard

Exit QEMU with :kbd:`Ctrl-a x`.

Modify the Kernel
=================

Now you can apply the driver patch and configure the kernel to use it.

Edit the linux-yocto kernel recipe:

.. code-block:: shell

   $ vi ~/kernel-lab-layers/meta-lab2-qemux86/recipes-kernel/linux/linux-yocto_&KERNEL_LAB_STABLE_VERSION;.bbappend

and uncomment the line including the patch and the line including the
lab2 config fragment:

.. code-block:: shell

   SRC_URI += "file://yocto-testmod.patch"
   SRC_URI += "file://lab2.cfg"

.. ********************************************************
   Maintainers:
     do not commit the modified linux-yocto*.bbappend, the
     recipes need to be in the state expected at the
     start of lab manual.
   ********************************************************

This accomplishes the same thing, adding and enabling the
``'yocto-testmod'`` module, that you accomplished in Lab 1. The
difference here is that instead of using :command:`menuconfig` to
enable the new option in the monolithic :file:`.config` file as in
Lab 1, here you add the patch in the same way but enable the test
module using the standalone :file:`lab2.cfg` config fragment.

Save your changes and close :command:`vi`.

Configure the Kernel
====================

You could use :command:`menuconfig` to enable the option, but since you
already know what it is, you can simply add it to the :file:`lab2.cfg`
file.

Open the file:

.. code-block:: shell

   $ vi ~/kernel-lab-layers/meta-lab2-qemux86/recipes-kernel/linux/files/lab2.cfg

and examine the following lines, which enable the module as a built-in
kernel module:

.. code-block:: shell

   # Enable the testmod
   CONFIG_YOCTO_TESTMOD=y

Close :command:`vi`.

.. tip::
   You know what you need to add now, but if you are not sure exactly
   which config option you need, you can save off the original
   :file:`.config` (after an initial ``linux-yocto`` build), then run
   :command:`menuconfig` and take a diff of the two files. You can then
   easily deduce what your config fragment should contain.

Now you can rebuild and boot the new kernel. Bitbake will detect the
recipe file has changed and start by fetching the new sources and apply
the patch:

.. code-block:: shell

   $ bitbake linux-yocto -c deploy
   $ runqemu nographic tmp/deploy/images/lab2-qemux86/bzImage-lab2-qemux86.bin tmp/deploy/images/lab2-qemux86/core-image-minimal-lab2-qemux86.ext4

Like before, QEMU will open a new window and boot to a login prompt.

As in Lab 1, you can scroll back through the boot log using
:kbd:`Shift+PgUp`. You should find the Yocto test driver message in
there or just grep for it:

.. code-block:: shell

   INIT: version 2.99 booting
   Starting udev
   [    3.533383] udevd[156]: starting version 3.2.10
   [    3.578257] udevd[157]: starting eudev-3.2.10
   [    4.155466] EXT4-fs (vda): re-mounted. Opts: (null). Quota mode: disabled.
   INIT: Entering runlevel: 5
   Configuring network interfaces... ip: RTNETLINK answers: File exists
   Starting syslogd/klogd: done
   
   Poky (Yocto Project Reference Distro) 3.4.3 lab2-qemux86 /dev/ttyS0
   
   lab2-qemux86 login: root
   root@lab2-qemux86:~# dmesg | grep Krillroy
   [    1.739235] Krillroy swam here!

Exit QEMU using :kbd:`Ctrl-a x`.


Modify the Kernel to Make Use of an LTS Kernel Option
=====================================================

.. note::
   This exercise shows how to enable support for caching block device
   access to MTD devices :file:`mtd-block.cfg` config option. This is
   very similar to the previous exercise in which you enabled the
   Yocto 'testmod' using the :file:`lab2.cfg` fragment.

We first need to switch to the &KERNEL_LAB_LTS_VERSION; kernel. Open
the machine configuration file for lab2 in :command:`vi`:

.. code-block:: shell

   $ vi ~/kernel-lab-layers/meta-lab2-qemux86/conf/machine/lab2-qemux86.conf

Change the preferred version of the ``linux-yocto kernel`` to
&KERNEL_LAB_LTS_VERSION; by commenting out the &KERNEL_LAB_STABLE_VERSION;
line and uncommenting the &KERNEL_LAB_LTS_VERSION; line as such:

.. code-block:: shell

   PREFERRED_PROVIDER_virtual/kernel ?= "linux-yocto"
   #PREFERRED_VERSION_linux-yocto ?= "&KERNEL_LAB_STABLE_VERSION;%"
   PREFERRED_VERSION_linux-yocto ?= "&KERNEL_LAB_LTS_VERSION;%"

.. ********************************************************
   Maintainers:
     do not commit the modified lab2-qemux86.conf, the
     machine config needs to be in the state expected at
     the start of lab manual.
   ********************************************************

Now you can rebuild and boot the new kernel:

.. code-block:: shell

   $ bitbake linux-yocto -c deploy
   $ runqemu nographic tmp/deploy/images/lab2-qemux86/bzImage-lab2-qemux86.bin tmp/deploy/images/lab2-qemux86/core-image-minimal-lab2-qemux86.ext4

Verify that you are in fact now running the &KERNEL_LAB_LTS_VERSION; kernel:

.. code-block:: shell

   # uname -r
   &KERNEL_LAB_LTS_FULL_VERSION;-yocto-standard

Configure the Kernel Again
==========================

You could use :command:`menuconfig` to enable the option, but since you
already know what it is, you can simply add it and its dependencies to
the :file:`mtd-block.cfg` file.

Open the :file:`mtd-block.cfg` file:

.. code-block:: shell

   $ vi ~/kernel-lab-layers/meta-lab2-qemux86/recipes-kernel/linux/files/mtd-block.cfg

and examine the following lines, which enable the built-in MTD BLOCK
config item:

.. code-block:: shell

   ## Enable MTD BLOCK
   CONFIG_MTD=y
   CONFIG_MTD_BLOCK=y

Close :command:`vi`.

Note that ``CONFIG_MTD`` needs to be enabled in order for
``CONFIG_MTD_BLOCK`` to be enabled.(The complete set of dependent
options required for a given option can be generated by taking the diff
between the kernel :file:`.config` before and after the option of
interest was enabled via ``‘bitbake -c menuconfig’`` as demonstrated
in previous labs.)

Because this option doesn't really produce an easily visible effect
such as a line in the qemu machine’s kernel log, we'll just verify
that the config fragment actually ends up taking effect in the kernel
build.

Open the kernel config file generated by the previous build:

.. code-block:: shell

   $ vi ~/poky/build/tmp/work/lab2_qemux86-poky-linux/linux-yocto/&KERNEL_LAB_LTS_FULL_VERSION;+gitAUTOINC+&KERNEL_LAB_LTS_KMETA_SHORT_HASH;_&KERNEL_LAB_LTS_KBRANCH_SHORT_HASH;-r0/linux-lab2_qemux86-standard-build/.config

and use the :guilabel:`Search | Find` menu item to search for the following config item:

.. code-block:: shell

   CONFIG_MTD

What you should find is that that config item is not set:

.. code-block:: shell

   # CONFIG_MTD is not set

Also, you shouldn’t see a ``CONFIG_MTD_BLOCK`` option at all, because
it depends on ``CONFIG_MTD``, which is disabled.

Edit the ``linux-yocto`` kernel recipe:

.. code-block:: shell

   $ vi ~/kernel-lab-layers/meta-lab2-qemux86/recipes-kernel/linux/linux-yocto_&KERNEL_LAB_LTS_VERSION;.bbappend

and uncomment the line including the built-in MTD BLOCK config
fragment:

.. code-block:: shell

   SRC_URI += "file://mtd-block.cfg"

Save your changes and close :command:`vi`.

.. ********************************************************
   Maintainers:
     do not commit the modified linux-yocto*.bbappend, the
     recipes need to be in the state expected at the
     start of lab manual.
   ********************************************************

Rebuild the Kernel
==================

Now you can rebuild and boot the new kernel:

.. code-block:: shell

   $ bitbake linux-yocto -c deploy
   $ runqemu nographic tmp/deploy/images/lab2-qemux86/bzImage-lab2-qemux86.bin tmp/deploy/images/lab2-qemux86/core-image-minimal-lab2-qemux86.ext4

Your kernel should boot without problem, and if you ran this on real
hardware, you'd expect to see support for built-in ``MTD BLOCK``
enabled and available. For the purposes of this lab, however, it's
sufficient to verify that the option actually took effect in the final
kernel configuration. You can verify that the ``MTD BLOCK`` support has been enabled in the kernel by again looking at the final kernel config
file after enabling the :file:`mtd-block.cfg` config fragment.

Open the config file:

.. code-block:: shell

   $ vi ~/poky/build/tmp/work/lab2_qemux86-poky-linux/linux-yocto/&KERNEL_LAB_LTS_FULL_VERSION;+gitAUTOINC+&KERNEL_LAB_LTS_KMETA_SHORT_HASH;_&KERNEL_LAB_LTS_KBRANCH_SHORT_HASH;-r0/linux-lab2_qemux86-standard-build/.config

and use the :guilabel:`Search | Find` menu item to search for the
following config items:

.. code-block:: shell

   CONFIG_MTD
   CONFIG_MTD_BLOCK

What you should find is that that those config items are now set:

.. code-block:: shell

   CONFIG_MTD=y
   ...
   CONFIG_MTD_BLOCK=y

Close :command:`vi`.

Lab 2 Conclusion
================

In this lab you applied a patch and modified the configuration of the
Linux kernel using a config fragment, which is a feature provided by
the ``linux-yocto`` kernel tooling.  You also switched kernel versions
and enabled a kernel option using a config fragment This concludes
Lab 2.

Extra Credit: Iterative Development
===================================

Should you need to modify the kernel further at this point, perhaps it
failed to compile or you want to experiment with the new driver, you
can do that directly using the sources in:

.. code-block:: shell

   $ cd ~/poky/build/tmp/work-shared/lab2-qemux86/kernel-source

.. tip::
   This is a great time to make use of that :kbd:`Tab` completion!

After making changes to the source, you can rebuild and test those
changes, just be careful not to run a clean, fetch, unpack or patch
task or you will lose your changes:

.. code-block:: shell

   $ cd ~/poky/build
   $ bitbake linux-yocto -c compile -f
   $ bitbake linux-yocto -c deploy
   $ runqemu nographic tmp/deploy/images/lab2-qemux86/bzImage-lab2-qemux86.bin tmp/deploy/images/lab2-qemux86/core-image-minimal-lab2-qemux86.ext4

You can repeat this cycle as needed until you are happy with the kernel
changes.

The ``linux-yocto`` recipe creates a git tree here, so once you are
done making your changes, you can easily save them off into a patch
using standard :command:`git` commands:

.. code-block:: shell

   $ git add path/to/file/you/change
   $ git commit -–signoff
   $ git format-patch -1

You can then integrate these patches into the layer by copying them
alongside the :file:`yocto-testmod.patch` and adding them to the
:term:`SRC_URI`.


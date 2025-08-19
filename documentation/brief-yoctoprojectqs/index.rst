.. SPDX-License-Identifier: CC-BY-SA-2.0-UK

=========================
Yocto Project Quick Build
=========================

Welcome!
========

This short document steps you through the process for a typical
image build using the Yocto Project. The document also introduces how to
configure a build for specific hardware. You will use Yocto Project to
build a reference embedded OS called Poky.

.. note::

   -  The examples in this paper assume you are using a native Linux
      system running a recent Ubuntu Linux distribution. If the machine
      you want to use Yocto Project on to build an image
      (:term:`Build Host`) is not
      a native Linux system, you can still perform these steps by using
      CROss PlatformS (CROPS) and setting up a Poky container. See the
      :ref:`dev-manual/start:setting up to use cross platforms (crops)`
      section
      in the Yocto Project Development Tasks Manual for more
      information.

   -  You may use version 2 of Windows Subsystem For Linux (WSL 2) to set
      up a build host using Windows 10 or later, Windows Server 2019 or later.
      See the :ref:`dev-manual/start:setting up to use windows subsystem for
      linux (wsl 2)` section in the Yocto Project Development Tasks Manual
      for more information.

If you want more conceptual or background information on the Yocto
Project, see the :doc:`/overview-manual/index`.

Compatible Linux Distribution
=============================

Make sure your :term:`Build Host` meets the
following requirements:

-  At least &MIN_DISK_SPACE; Gbytes of free disk space, though
   much more will help to run multiple builds and increase
   performance by reusing build artifacts.

-  At least &MIN_RAM; Gbytes of RAM, though a modern build host with as
   much RAM and as many CPU cores as possible is strongly recommended to
   maximize build performance.

-  Runs a supported Linux distribution (i.e. recent releases of Fedora,
   openSUSE, CentOS, Debian, or Ubuntu). For a list of Linux
   distributions that support the Yocto Project, see the
   :ref:`ref-manual/system-requirements:supported linux distributions`
   section in the Yocto Project Reference Manual. For detailed
   information on preparing your build host, see the
   :ref:`dev-manual/start:preparing the build host`
   section in the Yocto Project Development Tasks Manual.

-  Ensure that the following utilities have these minimum version numbers:

   -  Git &MIN_GIT_VERSION; or greater
   -  tar &MIN_TAR_VERSION; or greater
   -  Python &MIN_PYTHON_VERSION; or greater.
   -  gcc &MIN_GCC_VERSION; or greater.
   -  GNU make &MIN_MAKE_VERSION; or greater

If your build host does not satisfy all of the above version
requirements, you can take steps to prepare the system so that you
can still use the Yocto Project. See the
:ref:`ref-manual/system-requirements:required git, tar, python, make and gcc versions`
section in the Yocto Project Reference Manual for information.

Build Host Packages
===================

You must install essential host packages on your build host. The
following command installs the host packages based on an Ubuntu
distribution:

.. literalinclude:: ../tools/host_packages_scripts/ubuntu_essential.sh
   :language: shell

.. note::

   For host package requirements on all supported Linux distributions,
   see the :ref:`ref-manual/system-requirements:required packages for the build host`
   section in the Yocto Project Reference Manual.

Use Git to Clone bitbake-setup
==============================

Once you complete the setup instructions for your machine, you need to
get a copy of the bitbake-setup tool to setup the Poky reference
distribution on your build host. Use the following commands to clone
the bitbake repository.

.. code-block:: shell

   $ git clone git://git.openembedded.org/bitbake bitbake-setup
   Cloning into 'bitbake-setup'...
   remote: Enumerating objects: 68454, done.
   remote: Counting objects: 100% (49/49), done.
   remote: Compressing objects: 100% (44/44), done.
   remote: Total 68454 (delta 31), reused 5 (delta 5), pack-reused 68405 (from 1)
   Receiving objects: 100% (68454/68454), 14.17 MiB | 10.56 MiB/s, done.
   Resolving deltas: 100% (51776/51776), done.

Setup a build environment with the following command:

.. code-block:: shell

   $ ./bitbake-setup/bin/bitbake-setup init

By default, this will setup in $HOME/bitbake-builds. If you prefer to
setup your builds in a different directory, for example the current
directory, you can instead use the ``--top-dir`` argument:

.. code-block:: shell

  $ ./bitbake-setup/bin/bitbake-setup init --top-dir $PWD

`bitbake-setup init` is an interactive program by default and will ask
you to make some decisions. Depending on your answers, the choices may
differ from the examples below.

#. Choose a configuration (for example, ``yocto-master-options``):

   .. code-block:: shell

      Available configurations:
      0. yocto-master-nested-configs	(future) Official Yocto configurations: poky, poky-altcfg, poky-tiny, for qemux86-64 and arm64 (defined with nested configurations)
      1. yocto-master-options	(future) Official Yocto configurations: poky, poky-altcfg, poky-tiny, for qemux86-64, riscv64 and arm64 (defined with options)

      Please select one of the above configurations by its number:
      1

#. Choose a target machine (for example, ``qemux86-64``):

   .. code-block:: shell

      Selecting the only available bitbake configuration poky
      Available target machines:
      0. machine/qemux86-64
      1. machine/qemuarm64
      2. machine/qemuriscv64
      Please select one of the above options by its number:
      0

#. Choose a distribution (for example, ``poky``):

   .. code-block:: shell

      Available distributions:
      0. distro/poky
      1. distro/poky-altcfg
      2. distro/poky-tiny
      Please select one of the above options by its number:
      0
      Run 'bitbake-setup yocto-master-options poky distro/poky machine/qemux86-64' to select this configuration non-interactively.
      Initializing a build in /path/to/top-dir/yocto-master-options-poky-distro_poky-machine_qemux86-64
      Fetching layer/tool repository bitbake into /path/to/top-dir/yocto-master-options-poky-distro_poky-machine_qemux86-64/layers/bitbake
      Fetching layer/tool repository openembedded-core into /path/to/top-dir/yocto-master-options-poky-distro_poky-machine_qemux86-64/layers/openembedded-core
      Fetching layer/tool repository meta-yocto into /path/to/top-dir/yocto-master-options-poky-distro_poky-machine_qemux86-64/layers/meta-yocto
      Fetching layer/tool repository yocto-docs into /path/to/top-dir/yocto-master-options-poky-distro_poky-machine_qemux86-64/layers/yocto-docs
      ==============================
      Setting up bitbake configuration in /path/to/top-dir/yocto-master-options-poky-distro_poky-machine_qemux86-64/build
      This bitbake configuration provides: Poky reference distro build
      Usage instructions and additional information are in /path/to/top-dir/yocto-master-options-poky-distro_poky-machine_qemux86-64/build/README

If you prefer to run non-interactively, you could use a command
like the following:

.. code-block:: shell

   $ bitbake-setup yocto-master-options poky distro/poky machine/qemux86-64

Among other things, the script creates the :term:`Build Directory`, which is
``build`` in this case and is located in the "top-dir" directory.  The script
also clones the layers needed to build the Poky reference distribution, in the
``layers`` subdirectory. After the script runs, your current working directory
is set to the :term:`Build Directory`. Later, when the build completes, the
:term:`Build Directory` contains all the files created during the build.


Information about the build environment can be found in ``/path/to/top-dir/yocto-master-options-poky-distro_poky-machine_qemux86-64/build/README`` which should look something like the following:

.. code-block:: shell

   Poky reference distro build

   Additional information is in /path/to/top-dir/yocto-master-options-poky-distro_poky-machine_qemux86-64/build/conf/conf-summary.txt and /path/to/top-dir/yocto-master-options-poky-distro_poky-machine_qemux86-64/build/conf/conf-notes.txt

   Source the environment using '. /path/to/top-dir/yocto-master-options-poky-distro_poky-machine_qemux86-64/build/init-build-env' to run builds from the command line.
   The bitbake configuration files (local.conf, bblayers.conf and more) can be found in /path/to/top-dir/yocto-master-options-poky-distro_poky-machine_qemux86-64/build/conf

For more options and information about accessing Yocto Project related
repositories, see the
:ref:`dev-manual/start:locating yocto project source files`
section in the Yocto Project Development Tasks Manual.

Building Your Image
===================

Use the following steps to build your image. The build process creates
an entire Linux distribution, including the toolchain, from source.

.. note::

   -  If you are working behind a firewall and your build host is not
      set up for proxies, you could encounter problems with the build
      process when fetching source code (e.g. fetcher failures or Git
      failures).

   -  If you do not know your proxy settings, consult your local network
      infrastructure resources and get that information. A good starting
      point could also be to check your web browser settings. Finally,
      you can find more information on the
      ":yocto_wiki:`Working Behind a Network Proxy </Working_Behind_a_Network_Proxy>`"
      page of the Yocto Project Wiki.

#. **Initialize the Build Environment:**
   Run the ``init-build-env`` environment setup script within the build directory
   to define Yocto Project's build environment on your build host.

   .. code-block:: shell

      $ source /path/to/top-dir/yocto-master-options-poky-distro_poky-machine_qemux86-64/build/init-build-env
      Poky reference distro build

#. **Examine Your Auto Configuration File:** When you set up the build
   environment, an auto configuration file named ``auto.conf`` becomes
   available in aa ``conf`` subdirectory of the :term:`Build Directory`. For this
   example, the defaults are set to include three ``OE_FRAGMENTS``:
   ``core/yocto/sstate-mirror-cdn``, ``machine/qemux86-64`` and ``distro/poky``.
   These set up the environment similar to what was previously in the local
   configuration file named ``local.conf`` which is now largely empty.
   For more information on fragments, see :ref:`bitbake-user-manual/bitbake-user-manual-metadata:\`\`addfragments\`\` directive` in the Bitbake User Manual.

   ``core/yocto/sstate-mirror-cdn`` sets up :term:`BB_HASHSERVE_UPSTREAM` and
   :term:`SSTATE_MIRRORS`. The definition can be found in
   ``../layers/openembedded-core/meta/conf/fragments/yocto/sstate-mirror-cdn.conf``.

   .. code-block:: shell

      BB_CONF_FRAGMENT_SUMMARY = "Use prebuilt sstate artifacts for standard Yocto build configurations."
      BB_CONF_FRAGMENT_DESCRIPTION = "The Yocto Project has prebuilt artefacts available for standard build configurations. \
      This fragment enables their use. This will mean the build will query the \
      the network to check for artefacts at the start of builds, which does slow it down \
      initially but it will then speed up the builds by not having to build things if they are \
      present in the cache. It assumes you can download something faster than you can build it \
      which will depend on your network. \
      Note: For this to work you also need hash-equivalence passthrough to the matching server \
      "

      BB_HASHSERVE_UPSTREAM = 'wss://hashserv.yoctoproject.org/ws'
      SSTATE_MIRRORS ?= "file://.* http://sstate.yoctoproject.org/all/PATH;downloadfilename=PATH"

#. **Examine Your Local Configuration File:** When you set up the build
   environment, a local configuration file named ``local.conf`` becomes
   available in a ``conf`` subdirectory of the :term:`Build Directory`. For this
   example, the defaults are set to build for a ``qemux86-64`` target,
   which is suitable for emulation. The package manager used is set to
   the RPM package manager.

   .. tip::

      You can significantly speed up your build and guard against fetcher
      failures by using :ref:`overview-manual/concepts:shared state cache`
      mirrors and enabling :ref:`overview-manual/concepts:hash equivalence`.
      This way, you can use pre-built artifacts rather than building them.
      This is relevant only when your network and the server that you use
      can download these artifacts faster than you would be able to build them.

      To use such mirrors, ``bitbake-setup`` includes the following in your
	  ``conf/auto.conf`` file (or you can add it to ``conf/local.conf``) in
	  the :term:`Build Directory`::

            OE_FRAGMENTS += "core/yocto/sstate-mirror-cdn"

      The hash equivalence server needs the websockets python module version 9.1
      or later. Debian GNU/Linux 12 (Bookworm) and later, Fedora, CentOS Stream
      9 and later, and Ubuntu 22.04 (LTS) and later, all have a recent enough
      package. Other supported distributions need to get the module some other
      place than their package feed, e.g. via ``pip``.

#. **Start the Build:** Continue with the following command to build an OS
   image for the target, which is ``core-image-sato`` in this example:

   .. code-block:: shell

      $ bitbake core-image-sato

   For information on using the ``bitbake`` command, see the
   :ref:`overview-manual/concepts:bitbake` section in the Yocto Project Overview and
   Concepts Manual, or see
   :ref:`bitbake-user-manual/bitbake-user-manual-intro:the bitbake command`
   in the BitBake User Manual.

#. **Simulate Your Image Using QEMU:** Once this particular image is
   built, you can start QEMU, which is a Quick EMUlator that ships with
   the Yocto Project:

   .. code-block:: shell

      $ runqemu qemux86-64

   If you want to learn more about running QEMU, see the
   :ref:`dev-manual/qemu:using the quick emulator (qemu)` chapter in
   the Yocto Project Development Tasks Manual.

#. **Exit QEMU:** Exit QEMU by either clicking on the shutdown icon or by typing
   ``Ctrl-C`` in the QEMU transcript window from which you evoked QEMU.

Customizing Your Build for Specific Hardware
============================================

So far, all you have done is quickly built an image suitable for
emulation only. This section shows you how to customize your build for
specific hardware by adding a hardware layer into the Yocto Project
development environment.

In general, layers are repositories that contain related sets of
instructions and configurations that tell the Yocto Project what to do.
Isolating related metadata into functionally specific layers facilitates
modular development and makes it easier to reuse the layer metadata.

.. note::

   By convention, layer names start with the string "meta-".

Follow these steps to add a hardware layer:

#. **Find a Layer:** Many hardware layers are available. The Yocto Project
   :yocto_git:`Source Repositories <>` has many hardware layers.
   This example adds the
   `meta-altera <https://github.com/kraj/meta-altera>`__ hardware layer.

#. **Clone the Layer:** Use Git to make a local copy of the layer on your
   machine. You can put the copy in the top level of the copy of the
   Poky repository created earlier:

   .. code-block:: shell

      $ cd poky
      $ git clone https://github.com/kraj/meta-altera.git
      Cloning into 'meta-altera'...
      remote: Counting objects: 25170, done.
      remote: Compressing objects: 100% (350/350), done.
      remote: Total 25170 (delta 645), reused 719 (delta 538), pack-reused 24219
      Receiving objects: 100% (25170/25170), 41.02 MiB | 1.64 MiB/s, done.
      Resolving deltas: 100% (13385/13385), done.
      Checking connectivity... done.

   The hardware layer is now available
   next to other layers inside the Poky reference repository on your build
   host as ``meta-altera`` and contains all the metadata needed to
   support hardware from Altera, which is owned by Intel.

   .. note::

      It is recommended for layers to have a branch per Yocto Project release.
      Please make sure to checkout the layer branch supporting the Yocto Project
      release you're using.

#. **Change the Configuration to Build for a Specific Machine:** The
   :term:`MACHINE` variable in the
   ``local.conf`` file specifies the machine for the build. For this
   example, set the :term:`MACHINE` variable to ``cyclone5``. These
   configurations are used:
   https://github.com/kraj/meta-altera/blob/master/conf/machine/cyclone5.conf.

   .. note::

      See the "Examine Your Local Configuration File" step earlier for more
      information on configuring the build.

#. **Add Your Layer to the Layer Configuration File:** Before you can use
   a layer during a build, you must add it to your ``bblayers.conf``
   file, which is found in the :term:`Build Directory` ``conf`` directory.

   Use the ``bitbake-layers add-layer`` command to add the layer to the
   configuration file:

   .. code-block:: shell

      $ cd poky/build
      $ bitbake-layers add-layer ../meta-altera
      NOTE: Starting bitbake server...
      Parsing recipes: 100% |##################################################################| Time: 0:00:32
      Parsing of 918 .bb files complete (0 cached, 918 parsed). 1401 targets,
      123 skipped, 0 masked, 0 errors.

   You can find
   more information on adding layers in the
   :ref:`dev-manual/layers:adding a layer using the \`\`bitbake-layers\`\` script`
   section.

Completing these steps has added the ``meta-altera`` layer to your Yocto
Project development environment and configured it to build for the
``cyclone5`` machine.

.. note::

   The previous steps are for demonstration purposes only. If you were
   to attempt to build an image for the ``cyclone5`` machine, you should
   read the Altera ``README``.

Creating Your Own General Layer
===============================

Maybe you have an application or specific set of behaviors you need to
isolate. You can create your own general layer using the
``bitbake-layers create-layer`` command. The tool automates layer
creation by setting up a subdirectory with a ``layer.conf``
configuration file, a ``recipes-example`` subdirectory that contains an
``example.bb`` recipe, a licensing file, and a ``README``.

The following commands run the tool to create a layer named
``meta-mylayer`` in the ``poky`` directory:

.. code-block:: shell

   $ cd poky
   $ bitbake-layers create-layer meta-mylayer
   NOTE: Starting bitbake server...
   Add your new layer with 'bitbake-layers add-layer meta-mylayer'

For more information
on layers and how to create them, see the
:ref:`dev-manual/layers:creating a general layer using the \`\`bitbake-layers\`\` script`
section in the Yocto Project Development Tasks Manual.

Where To Go Next
================

Now that you have experienced using the Yocto Project, you might be
asking yourself "What now?". The Yocto Project has many sources of
information including the website, wiki pages, and user manuals:

-  **Website:** The :yocto_home:`Yocto Project Website <>` provides
   background information, the latest builds, breaking news, full
   development documentation, and access to a rich Yocto Project
   Development Community into which you can tap.

-  **Video Seminar:** The `Introduction to the Yocto Project and BitBake, Part 1
   <https://youtu.be/yuE7my3KOpo>`__ and
   `Introduction to the Yocto Project and BitBake, Part 2
   <https://youtu.be/iZ05TTyzGHk>`__ videos offer a video seminar
   introducing you to the most important aspects of developing a
   custom embedded Linux distribution with the Yocto Project.

-  **Yocto Project Overview and Concepts Manual:** The
   :doc:`/overview-manual/index` is a great
   place to start to learn about the Yocto Project. This manual
   introduces you to the Yocto Project and its development environment.
   The manual also provides conceptual information for various aspects
   of the Yocto Project.

-  **Yocto Project Wiki:** The :yocto_wiki:`Yocto Project Wiki <>`
   provides additional information on where to go next when ramping up
   with the Yocto Project, release information, project planning, and QA
   information.

-  **Yocto Project Mailing Lists:** Related mailing lists provide a forum
   for discussion, patch submission and announcements. There are several
   mailing lists grouped by topic. See the
   :ref:`ref-manual/resources:mailing lists`
   section in the Yocto Project Reference Manual for a complete list of
   Yocto Project mailing lists.

-  **Comprehensive List of Links and Other Documentation:** The
   :ref:`ref-manual/resources:links and related documentation`
   section in the Yocto Project Reference Manual provides a
   comprehensive list of all related links and other user documentation.

.. include:: /boilerplate.rst

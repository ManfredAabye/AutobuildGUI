import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import os
import json
from datetime import datetime

class AutobuildGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Autobuild Configuration Tool for Second Life Viewer")
        self.root.geometry("1200x800")
        
        # Configuration storage
        self.config = {
            'build': {}, 'configure': {}, 'edit': {}, 'install': {}, 
            'installables': {}, 'manifest': {}, 'package': {}, 
            'print': {}, 'source_environment': {}, 'uninstall': {}, 'upload': {}
        }
        
        # Create main container
        self.main_container = ttk.Frame(root)
        self.main_container.pack(fill=tk.BOTH, expand=True)
        
        # Create notebook for different sections
        self.notebook = ttk.Notebook(self.main_container)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Create tabs
        self.create_build_tab()
        self.create_configure_tab()
        self.create_edit_tab()
        self.create_install_tab()
        self.create_installables_tab()
        self.create_manifest_tab()
        self.create_package_tab()
        self.create_print_tab()
        self.create_source_environment_tab()
        self.create_uninstall_tab()
        self.create_upload_tab()
        
        # Create bottom panel for batch generation
        self.create_bottom_panel()
        
        # Load default config if exists
        self.load_default_config()
    
    def create_bottom_panel(self):
        bottom_panel = ttk.Frame(self.main_container)
        bottom_panel.pack(fill=tk.X, padx=5, pady=5)
        
        # Save/Load buttons
        btn_frame = ttk.Frame(bottom_panel)
        btn_frame.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(btn_frame, text="Save Config", command=self.save_config).pack(side=tk.LEFT, padx=2)
        ttk.Button(btn_frame, text="Load Config", command=self.load_config).pack(side=tk.LEFT, padx=2)
        
        # Generate Batch button
        ttk.Button(bottom_panel, text="Generate Batch File", command=self.generate_batch).pack(side=tk.RIGHT, padx=5)
        
        # Preview area
        self.preview_text = scrolledtext.ScrolledText(bottom_panel, height=10, wrap=tk.WORD)
        self.preview_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
    
    def create_build_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Build")
        
        # Standard options
        std_frame = ttk.LabelFrame(tab, text="Standard Options")
        std_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.build_debug = tk.BooleanVar()
        ttk.Checkbutton(std_frame, text="Debug", variable=self.build_debug).pack(side=tk.LEFT, padx=5)
        
        self.build_dry_run = tk.BooleanVar()
        ttk.Checkbutton(std_frame, text="Dry Run", variable=self.build_dry_run).pack(side=tk.LEFT, padx=5)
        
        self.build_verbose = tk.BooleanVar()
        ttk.Checkbutton(std_frame, text="Verbose", variable=self.build_verbose).pack(side=tk.LEFT, padx=5)
        
        self.build_quiet = tk.BooleanVar()
        ttk.Checkbutton(std_frame, text="Quiet", variable=self.build_quiet).pack(side=tk.LEFT, padx=5)
        
        # Command-specific options
        cmd_frame = ttk.LabelFrame(tab, text="Build Options")
        cmd_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(cmd_frame, text="Configuration:").grid(row=0, column=0, sticky=tk.W, padx=5)
        self.build_configuration = ttk.Combobox(cmd_frame, values=["Debug", "Release", "RelWithDebInfo"])
        self.build_configuration.grid(row=0, column=1, sticky=tk.W, padx=5)
        
        self.build_all_configs = tk.BooleanVar()
        ttk.Checkbutton(cmd_frame, text="Build all configurations", variable=self.build_all_configs).grid(row=1, column=0, columnspan=2, sticky=tk.W, padx=5)
        
        self.build_no_configure = tk.BooleanVar()
        ttk.Checkbutton(cmd_frame, text="Skip configure step", variable=self.build_no_configure).grid(row=2, column=0, columnspan=2, sticky=tk.W, padx=5)
        
        ttk.Label(cmd_frame, text="Build ID:").grid(row=3, column=0, sticky=tk.W, padx=5)
        self.build_id = ttk.Entry(cmd_frame)
        self.build_id.grid(row=3, column=1, sticky=tk.W, padx=5)
        
        ttk.Label(cmd_frame, text="Address Size:").grid(row=4, column=0, sticky=tk.W, padx=5)
        self.build_address_size = ttk.Combobox(cmd_frame, values=["32", "64"])
        self.build_address_size.grid(row=4, column=1, sticky=tk.W, padx=5)
        
        ttk.Label(cmd_frame, text="Additional Options:").grid(row=5, column=0, sticky=tk.W, padx=5)
        self.build_additional_options = ttk.Entry(cmd_frame, width=40)
        self.build_additional_options.grid(row=5, column=1, sticky=tk.W, padx=5)
    
    def create_configure_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Configure")
        
        # Standard options
        std_frame = ttk.LabelFrame(tab, text="Standard Options")
        std_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.configure_debug = tk.BooleanVar()
        ttk.Checkbutton(std_frame, text="Debug", variable=self.configure_debug).pack(side=tk.LEFT, padx=5)
        
        self.configure_dry_run = tk.BooleanVar()
        ttk.Checkbutton(std_frame, text="Dry Run", variable=self.configure_dry_run).pack(side=tk.LEFT, padx=5)
        
        self.configure_verbose = tk.BooleanVar()
        ttk.Checkbutton(std_frame, text="Verbose", variable=self.configure_verbose).pack(side=tk.LEFT, padx=5)
        
        self.configure_quiet = tk.BooleanVar()
        ttk.Checkbutton(std_frame, text="Quiet", variable=self.configure_quiet).pack(side=tk.LEFT, padx=5)
        
        # Command-specific options
        cmd_frame = ttk.LabelFrame(tab, text="Configure Options")
        cmd_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.configure_all_configs = tk.BooleanVar()
        ttk.Checkbutton(cmd_frame, text="Configure all configurations", variable=self.configure_all_configs).grid(row=0, column=0, columnspan=2, sticky=tk.W, padx=5)
        
        ttk.Label(cmd_frame, text="Configuration:").grid(row=1, column=0, sticky=tk.W, padx=5)
        self.configure_configuration = ttk.Combobox(cmd_frame, values=["Debug", "Release", "RelWithDebInfo"])
        self.configure_configuration.grid(row=1, column=1, sticky=tk.W, padx=5)
        
        ttk.Label(cmd_frame, text="Address Size:").grid(row=2, column=0, sticky=tk.W, padx=5)
        self.configure_address_size = ttk.Combobox(cmd_frame, values=["32", "64"])
        self.configure_address_size.grid(row=2, column=1, sticky=tk.W, padx=5)
        
        ttk.Label(cmd_frame, text="Additional Options:").grid(row=3, column=0, sticky=tk.W, padx=5)
        self.configure_additional_options = ttk.Entry(cmd_frame, width=40)
        self.configure_additional_options.grid(row=3, column=1, sticky=tk.W, padx=5)
    
    def create_edit_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Edit")
        
        # Subcommand selection
        subcmd_frame = ttk.LabelFrame(tab, text="Edit Subcommand")
        subcmd_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.edit_subcommand = tk.StringVar(value="build")
        ttk.Radiobutton(subcmd_frame, text="Build", variable=self.edit_subcommand, value="build").pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(subcmd_frame, text="Configure", variable=self.edit_subcommand, value="configure").pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(subcmd_frame, text="Package", variable=self.edit_subcommand, value="package").pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(subcmd_frame, text="Platform", variable=self.edit_subcommand, value="platform").pack(side=tk.LEFT, padx=5)
        
        # Standard options
        std_frame = ttk.LabelFrame(tab, text="Standard Options")
        std_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.edit_debug = tk.BooleanVar()
        ttk.Checkbutton(std_frame, text="Debug", variable=self.edit_debug).pack(side=tk.LEFT, padx=5)
        
        self.edit_dry_run = tk.BooleanVar()
        ttk.Checkbutton(std_frame, text="Dry Run", variable=self.edit_dry_run).pack(side=tk.LEFT, padx=5)
        
        self.edit_verbose = tk.BooleanVar()
        ttk.Checkbutton(std_frame, text="Verbose", variable=self.edit_verbose).pack(side=tk.LEFT, padx=5)
        
        self.edit_quiet = tk.BooleanVar()
        ttk.Checkbutton(std_frame, text="Quiet", variable=self.edit_quiet).pack(side=tk.LEFT, padx=5)
        
        # Edit options frame
        edit_frame = ttk.LabelFrame(tab, text="Edit Options")
        edit_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(edit_frame, text="Configuration File:").grid(row=0, column=0, sticky=tk.W, padx=5)
        self.edit_config_file = ttk.Entry(edit_frame, width=40)
        self.edit_config_file.grid(row=0, column=1, sticky=tk.W, padx=5)
        ttk.Button(edit_frame, text="Browse...", command=lambda: self.browse_file(self.edit_config_file)).grid(row=0, column=2, padx=5)
        
        self.edit_delete = tk.BooleanVar()
        ttk.Checkbutton(edit_frame, text="Delete configuration", variable=self.edit_delete).grid(row=1, column=0, columnspan=3, sticky=tk.W, padx=5)
        
        # Build-specific edit options
        self.build_edit_frame = ttk.LabelFrame(tab, text="Build Edit Options")
        self.build_edit_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(self.build_edit_frame, text="Build Command:").grid(row=0, column=0, sticky=tk.W, padx=5)
        self.edit_build_command = ttk.Entry(self.build_edit_frame, width=40)
        self.edit_build_command.grid(row=0, column=1, sticky=tk.W, padx=5)
        
        # Configure-specific edit options
        self.configure_edit_frame = ttk.LabelFrame(tab, text="Configure Edit Options")
        self.configure_edit_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(self.configure_edit_frame, text="Configure Command:").grid(row=0, column=0, sticky=tk.W, padx=5)
        self.edit_configure_command = ttk.Entry(self.configure_edit_frame, width=40)
        self.edit_configure_command.grid(row=0, column=1, sticky=tk.W, padx=5)
        
        # Package-specific edit options
        self.package_edit_frame = ttk.LabelFrame(tab, text="Package Edit Options")
        self.package_edit_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(self.package_edit_frame, text="Package Name:").grid(row=0, column=0, sticky=tk.W, padx=5)
        self.edit_package_name = ttk.Entry(self.package_edit_frame, width=40)
        self.edit_package_name.grid(row=0, column=1, sticky=tk.W, padx=5)
        
        # Platform-specific edit options
        self.platform_edit_frame = ttk.LabelFrame(tab, text="Platform Edit Options")
        self.platform_edit_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(self.platform_edit_frame, text="Platform Name:").grid(row=0, column=0, sticky=tk.W, padx=5)
        self.edit_platform_name = ttk.Combobox(self.platform_edit_frame, values=["windows", "linux", "darwin"])
        self.edit_platform_name.grid(row=0, column=1, sticky=tk.W, padx=5)
        
        # Hide all specific frames initially
        self.hide_all_edit_frames()
        self.edit_subcommand.trace_add('write', self.update_edit_frames)
    
    def hide_all_edit_frames(self):
        self.build_edit_frame.pack_forget()
        self.configure_edit_frame.pack_forget()
        self.package_edit_frame.pack_forget()
        self.platform_edit_frame.pack_forget()
    
    def update_edit_frames(self, *args):
        self.hide_all_edit_frames()
        subcmd = self.edit_subcommand.get()
        
        if subcmd == "build":
            self.build_edit_frame.pack(fill=tk.X, padx=5, pady=5)
        elif subcmd == "configure":
            self.configure_edit_frame.pack(fill=tk.X, padx=5, pady=5)
        elif subcmd == "package":
            self.package_edit_frame.pack(fill=tk.X, padx=5, pady=5)
        elif subcmd == "platform":
            self.platform_edit_frame.pack(fill=tk.X, padx=5, pady=5)
    
    def create_install_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Install")
        
        # Standard options
        std_frame = ttk.LabelFrame(tab, text="Standard Options")
        std_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.install_debug = tk.BooleanVar()
        ttk.Checkbutton(std_frame, text="Debug", variable=self.install_debug).pack(side=tk.LEFT, padx=5)
        
        self.install_dry_run = tk.BooleanVar()
        ttk.Checkbutton(std_frame, text="Dry Run", variable=self.install_dry_run).pack(side=tk.LEFT, padx=5)
        
        self.install_verbose = tk.BooleanVar()
        ttk.Checkbutton(std_frame, text="Verbose", variable=self.install_verbose).pack(side=tk.LEFT, padx=5)
        
        self.install_quiet = tk.BooleanVar()
        ttk.Checkbutton(std_frame, text="Quiet", variable=self.install_quiet).pack(side=tk.LEFT, padx=5)
        
        # Command-specific options
        cmd_frame = ttk.LabelFrame(tab, text="Install Options")
        cmd_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(cmd_frame, text="Config File:").grid(row=0, column=0, sticky=tk.W, padx=5)
        self.install_config_file = ttk.Entry(cmd_frame, width=40)
        self.install_config_file.grid(row=0, column=1, sticky=tk.W, padx=5)
        ttk.Button(cmd_frame, text="Browse...", command=lambda: self.browse_file(self.install_config_file)).grid(row=0, column=2, padx=5)
        
        ttk.Label(cmd_frame, text="Install Directory:").grid(row=1, column=0, sticky=tk.W, padx=5)
        self.install_dir = ttk.Entry(cmd_frame, width=40)
        self.install_dir.grid(row=1, column=1, sticky=tk.W, padx=5)
        ttk.Button(cmd_frame, text="Browse...", command=lambda: self.browse_directory(self.install_dir)).grid(row=1, column=2, padx=5)
        
        ttk.Label(cmd_frame, text="Manifest File:").grid(row=2, column=0, sticky=tk.W, padx=5)
        self.install_manifest_file = ttk.Entry(cmd_frame, width=40)
        self.install_manifest_file.grid(row=2, column=1, sticky=tk.W, padx=5)
        ttk.Button(cmd_frame, text="Browse...", command=lambda: self.browse_file(self.install_manifest_file)).grid(row=2, column=2, padx=5)
        
        self.install_export_manifest = tk.BooleanVar()
        ttk.Checkbutton(cmd_frame, text="Export manifest to stdout", variable=self.install_export_manifest).grid(row=3, column=0, columnspan=3, sticky=tk.W, padx=5)
        
        self.install_list = tk.BooleanVar()
        ttk.Checkbutton(cmd_frame, text="List archives", variable=self.install_list).grid(row=4, column=0, columnspan=3, sticky=tk.W, padx=5)
        
        self.install_list_installed = tk.BooleanVar()
        ttk.Checkbutton(cmd_frame, text="List installed packages", variable=self.install_list_installed).grid(row=5, column=0, columnspan=3, sticky=tk.W, padx=5)
        
        self.install_list_licenses = tk.BooleanVar()
        ttk.Checkbutton(cmd_frame, text="List licenses", variable=self.install_list_licenses).grid(row=6, column=0, columnspan=3, sticky=tk.W, padx=5)
        
        ttk.Label(cmd_frame, text="Platform:").grid(row=7, column=0, sticky=tk.W, padx=5)
        self.install_platform = ttk.Combobox(cmd_frame, values=["windows", "linux", "darwin"])
        self.install_platform.grid(row=7, column=1, sticky=tk.W, padx=5)
        
        # Packages to install
        pkg_frame = ttk.LabelFrame(tab, text="Packages to Install")
        pkg_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.packages_listbox = tk.Listbox(pkg_frame, selectmode=tk.MULTIPLE, height=6)
        self.packages_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        scrollbar = ttk.Scrollbar(pkg_frame, orient=tk.VERTICAL, command=self.packages_listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.packages_listbox.config(yscrollcommand=scrollbar.set)
        
        # Add some default packages
        default_packages = [
            "boost", "openssl", "zlib", "curl", "xml2", "fmod", "ogg", 
            "vorbis", "openal", "colladadom", "google-breakpad", "ndofdev"
        ]
        for pkg in default_packages:
            self.packages_listbox.insert(tk.END, pkg)
        
        # Package management buttons
        btn_frame = ttk.Frame(pkg_frame)
        btn_frame.pack(side=tk.RIGHT, padx=5)
        
        ttk.Button(btn_frame, text="Add", command=self.add_package).pack(fill=tk.X, pady=2)
        ttk.Button(btn_frame, text="Remove", command=self.remove_package).pack(fill=tk.X, pady=2)
    
    def add_package(self):
        new_pkg = simpledialog.askstring("Add Package", "Enter package name:")
        if new_pkg:
            self.packages_listbox.insert(tk.END, new_pkg)
    
    def remove_package(self):
        selected = self.packages_listbox.curselection()
        for idx in reversed(selected):
            self.packages_listbox.delete(idx)
    
    def create_installables_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Installables")
        
        # Standard options
        std_frame = ttk.LabelFrame(tab, text="Standard Options")
        std_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.installables_debug = tk.BooleanVar()
        ttk.Checkbutton(std_frame, text="Debug", variable=self.installables_debug).pack(side=tk.LEFT, padx=5)
        
        self.installables_dry_run = tk.BooleanVar()
        ttk.Checkbutton(std_frame, text="Dry Run", variable=self.installables_dry_run).pack(side=tk.LEFT, padx=5)
        
        self.installables_verbose = tk.BooleanVar()
        ttk.Checkbutton(std_frame, text="Verbose", variable=self.installables_verbose).pack(side=tk.LEFT, padx=5)
        
        self.installables_quiet = tk.BooleanVar()
        ttk.Checkbutton(std_frame, text="Quiet", variable=self.installables_quiet).pack(side=tk.LEFT, padx=5)
        
        # Command-specific options
        cmd_frame = ttk.LabelFrame(tab, text="Installables Options")
        cmd_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(cmd_frame, text="Config File:").grid(row=0, column=0, sticky=tk.W, padx=5)
        self.installables_config_file = ttk.Entry(cmd_frame, width=40)
        self.installables_config_file.grid(row=0, column=1, sticky=tk.W, padx=5)
        ttk.Button(cmd_frame, text="Browse...", command=lambda: self.browse_file(self.installables_config_file)).grid(row=0, column=2, padx=5)
        
        # Command selection
        cmd_select_frame = ttk.Frame(cmd_frame)
        cmd_select_frame.grid(row=1, column=0, columnspan=3, sticky=tk.W, padx=5, pady=5)
        
        self.installables_command = tk.StringVar(value="add")
        ttk.Radiobutton(cmd_select_frame, text="Add", variable=self.installables_command, value="add").pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(cmd_select_frame, text="Remove", variable=self.installables_command, value="remove").pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(cmd_select_frame, text="Edit", variable=self.installables_command, value="edit").pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(cmd_select_frame, text="Print", variable=self.installables_command, value="print").pack(side=tk.LEFT, padx=5)
        
        # Package details
        pkg_frame = ttk.LabelFrame(tab, text="Package Details")
        pkg_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        ttk.Label(pkg_frame, text="Package Name:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=2)
        self.installables_pkg_name = ttk.Entry(pkg_frame, width=40)
        self.installables_pkg_name.grid(row=0, column=1, sticky=tk.W, padx=5, pady=2)
        
        ttk.Label(pkg_frame, text="Credentials:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=2)
        self.installables_creds = ttk.Combobox(pkg_frame, values=["", "github", "gitlab"])
        self.installables_creds.grid(row=1, column=1, sticky=tk.W, padx=5, pady=2)
        
        ttk.Label(pkg_frame, text="URL:").grid(row=2, column=0, sticky=tk.W, padx=5, pady=2)
        self.installables_url = ttk.Entry(pkg_frame, width=40)
        self.installables_url.grid(row=2, column=1, sticky=tk.W, padx=5, pady=2)
        
        ttk.Label(pkg_frame, text="Hash:").grid(row=3, column=0, sticky=tk.W, padx=5, pady=2)
        self.installables_hash = ttk.Entry(pkg_frame, width=40)
        self.installables_hash.grid(row=3, column=1, sticky=tk.W, padx=5, pady=2)
        
        ttk.Label(pkg_frame, text="Hash Algorithm:").grid(row=4, column=0, sticky=tk.W, padx=5, pady=2)
        self.installables_hash_alg = ttk.Combobox(pkg_frame, values=["md5", "blake2b"])
        self.installables_hash_alg.grid(row=4, column=1, sticky=tk.W, padx=5, pady=2)
        
        ttk.Label(pkg_frame, text="Archive:").grid(row=5, column=0, sticky=tk.W, padx=5, pady=2)
        self.installables_archive = ttk.Entry(pkg_frame, width=40)
        self.installables_archive.grid(row=5, column=1, sticky=tk.W, padx=5, pady=2)
        ttk.Button(pkg_frame, text="Browse...", command=lambda: self.browse_file(self.installables_archive)).grid(row=5, column=2, padx=5, pady=2)
    
    def create_manifest_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Manifest")
        
        # Standard options
        std_frame = ttk.LabelFrame(tab, text="Standard Options")
        std_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.manifest_debug = tk.BooleanVar()
        ttk.Checkbutton(std_frame, text="Debug", variable=self.manifest_debug).pack(side=tk.LEFT, padx=5)
        
        self.manifest_dry_run = tk.BooleanVar()
        ttk.Checkbutton(std_frame, text="Dry Run", variable=self.manifest_dry_run).pack(side=tk.LEFT, padx=5)
        
        self.manifest_verbose = tk.BooleanVar()
        ttk.Checkbutton(std_frame, text="Verbose", variable=self.manifest_verbose).pack(side=tk.LEFT, padx=5)
        
        self.manifest_quiet = tk.BooleanVar()
        ttk.Checkbutton(std_frame, text="Quiet", variable=self.manifest_quiet).pack(side=tk.LEFT, padx=5)
        
        # Command-specific options
        cmd_frame = ttk.LabelFrame(tab, text="Manifest Options")
        cmd_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(cmd_frame, text="Config File:").grid(row=0, column=0, sticky=tk.W, padx=5)
        self.manifest_config_file = ttk.Entry(cmd_frame, width=40)
        self.manifest_config_file.grid(row=0, column=1, sticky=tk.W, padx=5)
        ttk.Button(cmd_frame, text="Browse...", command=lambda: self.browse_file(self.manifest_config_file)).grid(row=0, column=2, padx=5)
        
        ttk.Label(cmd_frame, text="Platform:").grid(row=1, column=0, sticky=tk.W, padx=5)
        self.manifest_platform = ttk.Combobox(cmd_frame, values=["windows", "linux", "darwin"])
        self.manifest_platform.grid(row=1, column=1, sticky=tk.W, padx=5)
        
        # Command selection
        cmd_select_frame = ttk.Frame(cmd_frame)
        cmd_select_frame.grid(row=2, column=0, columnspan=3, sticky=tk.W, padx=5, pady=5)
        
        self.manifest_command = tk.StringVar(value="add")
        ttk.Radiobutton(cmd_select_frame, text="Add", variable=self.manifest_command, value="add").pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(cmd_select_frame, text="Remove", variable=self.manifest_command, value="remove").pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(cmd_select_frame, text="Clear", variable=self.manifest_command, value="clear").pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(cmd_select_frame, text="Print", variable=self.manifest_command, value="print").pack(side=tk.LEFT, padx=5)
        
        # Patterns
        pattern_frame = ttk.LabelFrame(tab, text="Patterns")
        pattern_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.patterns_listbox = tk.Listbox(pattern_frame, selectmode=tk.MULTIPLE, height=6)
        self.patterns_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        scrollbar = ttk.Scrollbar(pattern_frame, orient=tk.VERTICAL, command=self.patterns_listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.patterns_listbox.config(yscrollcommand=scrollbar.set)
        
        # Add some default patterns
        default_patterns = [
            "*.exe", "*.dll", "*.so", "*.dylib", "*.ini", 
            "*.xml", "*.txt", "*.cfg", "*.dat"
        ]
        for pattern in default_patterns:
            self.patterns_listbox.insert(tk.END, pattern)
        
        # Pattern management buttons
        btn_frame = ttk.Frame(pattern_frame)
        btn_frame.pack(side=tk.RIGHT, padx=5)
        
        ttk.Button(btn_frame, text="Add", command=self.add_pattern).pack(fill=tk.X, pady=2)
        ttk.Button(btn_frame, text="Remove", command=self.remove_pattern).pack(fill=tk.X, pady=2)
    
    def add_pattern(self):
        new_pattern = simpledialog.askstring("Add Pattern", "Enter file pattern (e.g., *.dll):")
        if new_pattern:
            self.patterns_listbox.insert(tk.END, new_pattern)
    
    def remove_pattern(self):
        selected = self.patterns_listbox.curselection()
        for idx in reversed(selected):
            self.patterns_listbox.delete(idx)
    
    def create_package_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Package")
        
        # Standard options
        std_frame = ttk.LabelFrame(tab, text="Standard Options")
        std_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.package_debug = tk.BooleanVar()
        ttk.Checkbutton(std_frame, text="Debug", variable=self.package_debug).pack(side=tk.LEFT, padx=5)
        
        self.package_dry_run = tk.BooleanVar()
        ttk.Checkbutton(std_frame, text="Dry Run", variable=self.package_dry_run).pack(side=tk.LEFT, padx=5)
        
        self.package_verbose = tk.BooleanVar()
        ttk.Checkbutton(std_frame, text="Verbose", variable=self.package_verbose).pack(side=tk.LEFT, padx=5)
        
        self.package_quiet = tk.BooleanVar()
        ttk.Checkbutton(std_frame, text="Quiet", variable=self.package_quiet).pack(side=tk.LEFT, padx=5)
        
        # Command-specific options
        cmd_frame = ttk.LabelFrame(tab, text="Package Options")
        cmd_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(cmd_frame, text="Config File:").grid(row=0, column=0, sticky=tk.W, padx=5)
        self.package_config_file = ttk.Entry(cmd_frame, width=40)
        self.package_config_file.grid(row=0, column=1, sticky=tk.W, padx=5)
        ttk.Button(cmd_frame, text="Browse...", command=lambda: self.browse_file(self.package_config_file)).grid(row=0, column=2, padx=5)
        
        ttk.Label(cmd_frame, text="Archive Name:").grid(row=1, column=0, sticky=tk.W, padx=5)
        self.package_archive_name = ttk.Entry(cmd_frame, width=40)
        self.package_archive_name.grid(row=1, column=1, sticky=tk.W, padx=5)
        
        ttk.Label(cmd_frame, text="Platform:").grid(row=2, column=0, sticky=tk.W, padx=5)
        self.package_platform = ttk.Combobox(cmd_frame, values=["windows", "linux", "darwin"])
        self.package_platform.grid(row=2, column=1, sticky=tk.W, padx=5)
    
    def create_print_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Print")
        
        # Standard options
        std_frame = ttk.LabelFrame(tab, text="Standard Options")
        std_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.print_debug = tk.BooleanVar()
        ttk.Checkbutton(std_frame, text="Debug", variable=self.print_debug).pack(side=tk.LEFT, padx=5)
        
        self.print_dry_run = tk.BooleanVar()
        ttk.Checkbutton(std_frame, text="Dry Run", variable=self.print_dry_run).pack(side=tk.LEFT, padx=5)
        
        self.print_verbose = tk.BooleanVar()
        ttk.Checkbutton(std_frame, text="Verbose", variable=self.print_verbose).pack(side=tk.LEFT, padx=5)
        
        self.print_quiet = tk.BooleanVar()
        ttk.Checkbutton(std_frame, text="Quiet", variable=self.print_quiet).pack(side=tk.LEFT, padx=5)
        
        # Command-specific options
        cmd_frame = ttk.LabelFrame(tab, text="Print Options")
        cmd_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(cmd_frame, text="Config File:").grid(row=0, column=0, sticky=tk.W, padx=5)
        self.print_config_file = ttk.Entry(cmd_frame, width=40)
        self.print_config_file.grid(row=0, column=1, sticky=tk.W, padx=5)
        ttk.Button(cmd_frame, text="Browse...", command=lambda: self.browse_file(self.print_config_file)).grid(row=0, column=2, padx=5)
        
        self.print_json = tk.BooleanVar()
        ttk.Checkbutton(cmd_frame, text="Output as JSON", variable=self.print_json).grid(row=1, column=0, columnspan=3, sticky=tk.W, padx=5)
    
    def create_source_environment_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Source Environment")
        
        # Standard options
        std_frame = ttk.LabelFrame(tab, text="Standard Options")
        std_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.source_debug = tk.BooleanVar()
        ttk.Checkbutton(std_frame, text="Debug", variable=self.source_debug).pack(side=tk.LEFT, padx=5)
        
        self.source_dry_run = tk.BooleanVar()
        ttk.Checkbutton(std_frame, text="Dry Run", variable=self.source_dry_run).pack(side=tk.LEFT, padx=5)
        
        self.source_verbose = tk.BooleanVar()
        ttk.Checkbutton(std_frame, text="Verbose", variable=self.source_verbose).pack(side=tk.LEFT, padx=5)
        
        self.source_quiet = tk.BooleanVar()
        ttk.Checkbutton(std_frame, text="Quiet", variable=self.source_quiet).pack(side=tk.LEFT, padx=5)
        
        # Command-specific options
        cmd_frame = ttk.LabelFrame(tab, text="Source Environment Options")
        cmd_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(cmd_frame, text="Variables File:").grid(row=0, column=0, sticky=tk.W, padx=5)
        self.source_vars_file = ttk.Entry(cmd_frame, width=40)
        self.source_vars_file.grid(row=0, column=1, sticky=tk.W, padx=5)
        ttk.Button(cmd_frame, text="Browse...", command=lambda: self.browse_file(self.source_vars_file)).grid(row=0, column=2, padx=5)
    
    def create_uninstall_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Uninstall")
        
        # Standard options
        std_frame = ttk.LabelFrame(tab, text="Standard Options")
        std_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.uninstall_debug = tk.BooleanVar()
        ttk.Checkbutton(std_frame, text="Debug", variable=self.uninstall_debug).pack(side=tk.LEFT, padx=5)
        
        self.uninstall_dry_run = tk.BooleanVar()
        ttk.Checkbutton(std_frame, text="Dry Run", variable=self.uninstall_dry_run).pack(side=tk.LEFT, padx=5)
        
        self.uninstall_verbose = tk.BooleanVar()
        ttk.Checkbutton(std_frame, text="Verbose", variable=self.uninstall_verbose).pack(side=tk.LEFT, padx=5)
        
        self.uninstall_quiet = tk.BooleanVar()
        ttk.Checkbutton(std_frame, text="Quiet", variable=self.uninstall_quiet).pack(side=tk.LEFT, padx=5)
        
        # Command-specific options
        cmd_frame = ttk.LabelFrame(tab, text="Uninstall Options")
        cmd_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(cmd_frame, text="Config File:").grid(row=0, column=0, sticky=tk.W, padx=5)
        self.uninstall_config_file = ttk.Entry(cmd_frame, width=40)
        self.uninstall_config_file.grid(row=0, column=1, sticky=tk.W, padx=5)
        ttk.Button(cmd_frame, text="Browse...", command=lambda: self.browse_file(self.uninstall_config_file)).grid(row=0, column=2, padx=5)
        
        ttk.Label(cmd_frame, text="Install Directory:").grid(row=1, column=0, sticky=tk.W, padx=5)
        self.uninstall_dir = ttk.Entry(cmd_frame, width=40)
        self.uninstall_dir.grid(row=1, column=1, sticky=tk.W, padx=5)
        ttk.Button(cmd_frame, text="Browse...", command=lambda: self.browse_directory(self.uninstall_dir)).grid(row=1, column=2, padx=5)
        
        ttk.Label(cmd_frame, text="Manifest File:").grid(row=2, column=0, sticky=tk.W, padx=5)
        self.uninstall_manifest_file = ttk.Entry(cmd_frame, width=40)
        self.uninstall_manifest_file.grid(row=2, column=1, sticky=tk.W, padx=5)
        ttk.Button(cmd_frame, text="Browse...", command=lambda: self.browse_file(self.uninstall_manifest_file)).grid(row=2, column=2, padx=5)
        
        # Packages to uninstall
        pkg_frame = ttk.LabelFrame(tab, text="Packages to Uninstall")
        pkg_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.uninstall_packages_listbox = tk.Listbox(pkg_frame, selectmode=tk.MULTIPLE, height=6)
        self.uninstall_packages_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        scrollbar = ttk.Scrollbar(pkg_frame, orient=tk.VERTICAL, command=self.uninstall_packages_listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.uninstall_packages_listbox.config(yscrollcommand=scrollbar.set)
        
        # Add some default packages
        default_packages = [
            "boost", "openssl", "zlib", "curl", "xml2", "fmod", "ogg", 
            "vorbis", "openal", "colladadom", "google-breakpad", "ndofdev"
        ]
        for pkg in default_packages:
            self.uninstall_packages_listbox.insert(tk.END, pkg)
        
        # Package management buttons
        btn_frame = ttk.Frame(pkg_frame)
        btn_frame.pack(side=tk.RIGHT, padx=5)
        
        ttk.Button(btn_frame, text="Add", command=self.add_uninstall_package).pack(fill=tk.X, pady=2)
        ttk.Button(btn_frame, text="Remove", command=self.remove_uninstall_package).pack(fill=tk.X, pady=2)
    
    def add_uninstall_package(self):
        new_pkg = simpledialog.askstring("Add Package", "Enter package name:")
        if new_pkg:
            self.uninstall_packages_listbox.insert(tk.END, new_pkg)
    
    def remove_uninstall_package(self):
        selected = self.uninstall_packages_listbox.curselection()
        for idx in reversed(selected):
            self.uninstall_packages_listbox.delete(idx)
    
    def create_upload_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Upload")
        
        # Standard options
        std_frame = ttk.LabelFrame(tab, text="Standard Options")
        std_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.upload_debug = tk.BooleanVar()
        ttk.Checkbutton(std_frame, text="Debug", variable=self.upload_debug).pack(side=tk.LEFT, padx=5)
        
        self.upload_dry_run = tk.BooleanVar()
        ttk.Checkbutton(std_frame, text="Dry Run", variable=self.upload_dry_run).pack(side=tk.LEFT, padx=5)
        
        self.upload_verbose = tk.BooleanVar()
        ttk.Checkbutton(std_frame, text="Verbose", variable=self.upload_verbose).pack(side=tk.LEFT, padx=5)
        
        self.upload_quiet = tk.BooleanVar()
        ttk.Checkbutton(std_frame, text="Quiet", variable=self.upload_quiet).pack(side=tk.LEFT, padx=5)
        
        # Command-specific options
        cmd_frame = ttk.LabelFrame(tab, text="Upload Options")
        cmd_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(cmd_frame, text="Archive File:").grid(row=0, column=0, sticky=tk.W, padx=5)
        self.upload_archive = ttk.Entry(cmd_frame, width=40)
        self.upload_archive.grid(row=0, column=1, sticky=tk.W, padx=5)
        ttk.Button(cmd_frame, text="Browse...", command=lambda: self.browse_file(self.upload_archive)).grid(row=0, column=2, padx=5)
        
        self.upload_to_s3 = tk.BooleanVar()
        ttk.Checkbutton(cmd_frame, text="Upload to S3", variable=self.upload_to_s3).grid(row=1, column=0, columnspan=3, sticky=tk.W, padx=5)
        
        ttk.Label(cmd_frame, text="Credentials File:").grid(row=2, column=0, sticky=tk.W, padx=5)
        self.upload_credentials = ttk.Entry(cmd_frame, width=40)
        self.upload_credentials.grid(row=2, column=1, sticky=tk.W, padx=5)
        ttk.Button(cmd_frame, text="Browse...", command=lambda: self.browse_file(self.upload_credentials)).grid(row=2, column=2, padx=5)
    
    def browse_file(self, entry_widget):
        filename = filedialog.askopenfilename()
        if filename:
            entry_widget.delete(0, tk.END)
            entry_widget.insert(0, filename)
    
    def browse_directory(self, entry_widget):
        dirname = filedialog.askdirectory()
        if dirname:
            entry_widget.delete(0, tk.END)
            entry_widget.insert(0, dirname)
    
    def save_config(self):
        filename = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
        if filename:
            self.collect_config_data()
            try:
                with open(filename, 'w') as f:
                    json.dump(self.config, f, indent=4)
                messagebox.showinfo("Success", "Configuration saved successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save configuration: {str(e)}")
    
    def load_config(self):
        filename = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if filename:
            try:
                with open(filename, 'r') as f:
                    self.config = json.load(f)
                self.apply_config_data()
                messagebox.showinfo("Success", "Configuration loaded successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load configuration: {str(e)}")
    
    def load_default_config(self):
        # Try to load default config if it exists
        default_config = "autobuild_config.json"
        if os.path.exists(default_config):
            try:
                with open(default_config, 'r') as f:
                    self.config = json.load(f)
                self.apply_config_data()
            except:
                pass  # Silently fail if default config can't be loaded
    
    def collect_config_data(self):
        # Build tab
        self.config['build'] = {
            'debug': self.build_debug.get(),
            'dry_run': self.build_dry_run.get(),
            'verbose': self.build_verbose.get(),
            'quiet': self.build_quiet.get(),
            'configuration': self.build_configuration.get(),
            'all_configs': self.build_all_configs.get(),
            'no_configure': self.build_no_configure.get(),
            'build_id': self.build_id.get(),
            'address_size': self.build_address_size.get(),
            'additional_options': self.build_additional_options.get()
        }
        
        # Configure tab
        self.config['configure'] = {
            'debug': self.configure_debug.get(),
            'dry_run': self.configure_dry_run.get(),
            'verbose': self.configure_verbose.get(),
            'quiet': self.configure_quiet.get(),
            'all_configs': self.configure_all_configs.get(),
            'configuration': self.configure_configuration.get(),
            'address_size': self.configure_address_size.get(),
            'additional_options': self.configure_additional_options.get()
        }
        
        # Edit tab
        self.config['edit'] = {
            'debug': self.edit_debug.get(),
            'dry_run': self.edit_dry_run.get(),
            'verbose': self.edit_verbose.get(),
            'quiet': self.edit_quiet.get(),
            'subcommand': self.edit_subcommand.get(),
            'config_file': self.edit_config_file.get(),
            'delete': self.edit_delete.get(),
            'build_command': self.edit_build_command.get(),
            'configure_command': self.edit_configure_command.get(),
            'package_name': self.edit_package_name.get(),
            'platform_name': self.edit_platform_name.get()
        }
        
        # Install tab
        self.config['install'] = {
            'debug': self.install_debug.get(),
            'dry_run': self.install_dry_run.get(),
            'verbose': self.install_verbose.get(),
            'quiet': self.install_quiet.get(),
            'config_file': self.install_config_file.get(),
            'install_dir': self.install_dir.get(),
            'manifest_file': self.install_manifest_file.get(),
            'export_manifest': self.install_export_manifest.get(),
            'list': self.install_list.get(),
            'list_installed': self.install_list_installed.get(),
            'list_licenses': self.install_list_licenses.get(),
            'platform': self.install_platform.get(),
            'packages': list(self.packages_listbox.get(0, tk.END))
        }
        
        # Installables tab
        self.config['installables'] = {
            'debug': self.installables_debug.get(),
            'dry_run': self.installables_dry_run.get(),
            'verbose': self.installables_verbose.get(),
            'quiet': self.installables_quiet.get(),
            'config_file': self.installables_config_file.get(),
            'command': self.installables_command.get(),
            'pkg_name': self.installables_pkg_name.get(),
            'creds': self.installables_creds.get(),
            'url': self.installables_url.get(),
            'hash': self.installables_hash.get(),
            'hash_alg': self.installables_hash_alg.get(),
            'archive': self.installables_archive.get()
        }
        
        # Manifest tab
        self.config['manifest'] = {
            'debug': self.manifest_debug.get(),
            'dry_run': self.manifest_dry_run.get(),
            'verbose': self.manifest_verbose.get(),
            'quiet': self.manifest_quiet.get(),
            'config_file': self.manifest_config_file.get(),
            'platform': self.manifest_platform.get(),
            'command': self.manifest_command.get(),
            'patterns': list(self.patterns_listbox.get(0, tk.END))
        }
        
        # Package tab
        self.config['package'] = {
            'debug': self.package_debug.get(),
            'dry_run': self.package_dry_run.get(),
            'verbose': self.package_verbose.get(),
            'quiet': self.package_quiet.get(),
            'config_file': self.package_config_file.get(),
            'archive_name': self.package_archive_name.get(),
            'platform': self.package_platform.get()
        }
        
        # Print tab
        self.config['print'] = {
            'debug': self.print_debug.get(),
            'dry_run': self.print_dry_run.get(),
            'verbose': self.print_verbose.get(),
            'quiet': self.print_quiet.get(),
            'config_file': self.print_config_file.get(),
            'json': self.print_json.get()
        }
        
        # Source Environment tab
        self.config['source_environment'] = {
            'debug': self.source_debug.get(),
            'dry_run': self.source_dry_run.get(),
            'verbose': self.source_verbose.get(),
            'quiet': self.source_quiet.get(),
            'vars_file': self.source_vars_file.get()
        }
        
        # Uninstall tab
        self.config['uninstall'] = {
            'debug': self.uninstall_debug.get(),
            'dry_run': self.uninstall_dry_run.get(),
            'verbose': self.uninstall_verbose.get(),
            'quiet': self.uninstall_quiet.get(),
            'config_file': self.uninstall_config_file.get(),
            'install_dir': self.uninstall_dir.get(),
            'manifest_file': self.uninstall_manifest_file.get(),
            'packages': list(self.uninstall_packages_listbox.get(0, tk.END))
        }
        
        # Upload tab
        self.config['upload'] = {
            'debug': self.upload_debug.get(),
            'dry_run': self.upload_dry_run.get(),
            'verbose': self.upload_verbose.get(),
            'quiet': self.upload_quiet.get(),
            'archive': self.upload_archive.get(),
            'to_s3': self.upload_to_s3.get(),
            'credentials': self.upload_credentials.get()
        }
    
    def apply_config_data(self):
        # Build tab
        build_cfg = self.config.get('build', {})
        self.build_debug.set(build_cfg.get('debug', False))
        self.build_dry_run.set(build_cfg.get('dry_run', False))
        self.build_verbose.set(build_cfg.get('verbose', False))
        self.build_quiet.set(build_cfg.get('quiet', False))
        self.build_configuration.set(build_cfg.get('configuration', ''))
        self.build_all_configs.set(build_cfg.get('all_configs', False))
        self.build_no_configure.set(build_cfg.get('no_configure', False))
        self.build_id.delete(0, tk.END)
        self.build_id.insert(0, build_cfg.get('build_id', ''))
        self.build_address_size.set(build_cfg.get('address_size', ''))
        self.build_additional_options.delete(0, tk.END)
        self.build_additional_options.insert(0, build_cfg.get('additional_options', ''))
        
        # Configure tab
        configure_cfg = self.config.get('configure', {})
        self.configure_debug.set(configure_cfg.get('debug', False))
        self.configure_dry_run.set(configure_cfg.get('dry_run', False))
        self.configure_verbose.set(configure_cfg.get('verbose', False))
        self.configure_quiet.set(configure_cfg.get('quiet', False))
        self.configure_all_configs.set(configure_cfg.get('all_configs', False))
        self.configure_configuration.set(configure_cfg.get('configuration', ''))
        self.configure_address_size.set(configure_cfg.get('address_size', ''))
        self.configure_additional_options.delete(0, tk.END)
        self.configure_additional_options.insert(0, configure_cfg.get('additional_options', ''))
        
        # Edit tab
        edit_cfg = self.config.get('edit', {})
        self.edit_debug.set(edit_cfg.get('debug', False))
        self.edit_dry_run.set(edit_cfg.get('dry_run', False))
        self.edit_verbose.set(edit_cfg.get('verbose', False))
        self.edit_quiet.set(edit_cfg.get('quiet', False))
        self.edit_subcommand.set(edit_cfg.get('subcommand', 'build'))
        self.edit_config_file.delete(0, tk.END)
        self.edit_config_file.insert(0, edit_cfg.get('config_file', ''))
        self.edit_delete.set(edit_cfg.get('delete', False))
        self.edit_build_command.delete(0, tk.END)
        self.edit_build_command.insert(0, edit_cfg.get('build_command', ''))
        self.edit_configure_command.delete(0, tk.END)
        self.edit_configure_command.insert(0, edit_cfg.get('configure_command', ''))
        self.edit_package_name.delete(0, tk.END)
        self.edit_package_name.insert(0, edit_cfg.get('package_name', ''))
        self.edit_platform_name.set(edit_cfg.get('platform_name', ''))
        
        # Install tab
        install_cfg = self.config.get('install', {})
        self.install_debug.set(install_cfg.get('debug', False))
        self.install_dry_run.set(install_cfg.get('dry_run', False))
        self.install_verbose.set(install_cfg.get('verbose', False))
        self.install_quiet.set(install_cfg.get('quiet', False))
        self.install_config_file.delete(0, tk.END)
        self.install_config_file.insert(0, install_cfg.get('config_file', ''))
        self.install_dir.delete(0, tk.END)
        self.install_dir.insert(0, install_cfg.get('install_dir', ''))
        self.install_manifest_file.delete(0, tk.END)
        self.install_manifest_file.insert(0, install_cfg.get('manifest_file', ''))
        self.install_export_manifest.set(install_cfg.get('export_manifest', False))
        self.install_list.set(install_cfg.get('list', False))
        self.install_list_installed.set(install_cfg.get('list_installed', False))
        self.install_list_licenses.set(install_cfg.get('list_licenses', False))
        self.install_platform.set(install_cfg.get('platform', ''))
        
        # Update packages listbox
        self.packages_listbox.delete(0, tk.END)
        for pkg in install_cfg.get('packages', []):
            self.packages_listbox.insert(tk.END, pkg)
        
        # Installables tab
        installables_cfg = self.config.get('installables', {})
        self.installables_debug.set(installables_cfg.get('debug', False))
        self.installables_dry_run.set(installables_cfg.get('dry_run', False))
        self.installables_verbose.set(installables_cfg.get('verbose', False))
        self.installables_quiet.set(installables_cfg.get('quiet', False))
        self.installables_config_file.delete(0, tk.END)
        self.installables_config_file.insert(0, installables_cfg.get('config_file', ''))
        self.installables_command.set(installables_cfg.get('command', 'add'))
        self.installables_pkg_name.delete(0, tk.END)
        self.installables_pkg_name.insert(0, installables_cfg.get('pkg_name', ''))
        self.installables_creds.set(installables_cfg.get('creds', ''))
        self.installables_url.delete(0, tk.END)
        self.installables_url.insert(0, installables_cfg.get('url', ''))
        self.installables_hash.delete(0, tk.END)
        self.installables_hash.insert(0, installables_cfg.get('hash', ''))
        self.installables_hash_alg.set(installables_cfg.get('hash_alg', ''))
        self.installables_archive.delete(0, tk.END)
        self.installables_archive.insert(0, installables_cfg.get('archive', ''))
        
        # Manifest tab
        manifest_cfg = self.config.get('manifest', {})
        self.manifest_debug.set(manifest_cfg.get('debug', False))
        self.manifest_dry_run.set(manifest_cfg.get('dry_run', False))
        self.manifest_verbose.set(manifest_cfg.get('verbose', False))
        self.manifest_quiet.set(manifest_cfg.get('quiet', False))
        self.manifest_config_file.delete(0, tk.END)
        self.manifest_config_file.insert(0, manifest_cfg.get('config_file', ''))
        self.manifest_platform.set(manifest_cfg.get('platform', ''))
        self.manifest_command.set(manifest_cfg.get('command', 'add'))
        
        # Update patterns listbox
        self.patterns_listbox.delete(0, tk.END)
        for pattern in manifest_cfg.get('patterns', []):
            self.patterns_listbox.insert(tk.END, pattern)
        
        # Package tab
        package_cfg = self.config.get('package', {})
        self.package_debug.set(package_cfg.get('debug', False))
        self.package_dry_run.set(package_cfg.get('dry_run', False))
        self.package_verbose.set(package_cfg.get('verbose', False))
        self.package_quiet.set(package_cfg.get('quiet', False))
        self.package_config_file.delete(0, tk.END)
        self.package_config_file.insert(0, package_cfg.get('config_file', ''))
        self.package_archive_name.delete(0, tk.END)
        self.package_archive_name.insert(0, package_cfg.get('archive_name', ''))
        self.package_platform.set(package_cfg.get('platform', ''))
        
        # Print tab
        print_cfg = self.config.get('print', {})
        self.print_debug.set(print_cfg.get('debug', False))
        self.print_dry_run.set(print_cfg.get('dry_run', False))
        self.print_verbose.set(print_cfg.get('verbose', False))
        self.print_quiet.set(print_cfg.get('quiet', False))
        self.print_config_file.delete(0, tk.END)
        self.print_config_file.insert(0, print_cfg.get('config_file', ''))
        self.print_json.set(print_cfg.get('json', False))
        
        # Source Environment tab
        source_cfg = self.config.get('source_environment', {})
        self.source_debug.set(source_cfg.get('debug', False))
        self.source_dry_run.set(source_cfg.get('dry_run', False))
        self.source_verbose.set(source_cfg.get('verbose', False))
        self.source_quiet.set(source_cfg.get('quiet', False))
        self.source_vars_file.delete(0, tk.END)
        self.source_vars_file.insert(0, source_cfg.get('vars_file', ''))
        
        # Uninstall tab
        uninstall_cfg = self.config.get('uninstall', {})
        self.uninstall_debug.set(uninstall_cfg.get('debug', False))
        self.uninstall_dry_run.set(uninstall_cfg.get('dry_run', False))
        self.uninstall_verbose.set(uninstall_cfg.get('verbose', False))
        self.uninstall_quiet.set(uninstall_cfg.get('quiet', False))
        self.uninstall_config_file.delete(0, tk.END)
        self.uninstall_config_file.insert(0, uninstall_cfg.get('config_file', ''))
        self.uninstall_dir.delete(0, tk.END)
        self.uninstall_dir.insert(0, uninstall_cfg.get('install_dir', ''))
        self.uninstall_manifest_file.delete(0, tk.END)
        self.uninstall_manifest_file.insert(0, uninstall_cfg.get('manifest_file', ''))
        
        # Update uninstall packages listbox
        self.uninstall_packages_listbox.delete(0, tk.END)
        for pkg in uninstall_cfg.get('packages', []):
            self.uninstall_packages_listbox.insert(tk.END, pkg)
        
        # Upload tab
        upload_cfg = self.config.get('upload', {})
        self.upload_debug.set(upload_cfg.get('debug', False))
        self.upload_dry_run.set(upload_cfg.get('dry_run', False))
        self.upload_verbose.set(upload_cfg.get('verbose', False))
        self.upload_quiet.set(upload_cfg.get('quiet', False))
        self.upload_archive.delete(0, tk.END)
        self.upload_archive.insert(0, upload_cfg.get('archive', ''))
        self.upload_to_s3.set(upload_cfg.get('to_s3', False))
        self.upload_credentials.delete(0, tk.END)
        self.upload_credentials.insert(0, upload_cfg.get('credentials', ''))
    
    def generate_batch(self):
        self.collect_config_data()
        batch_content = "@echo off\n"
        batch_content += ":: Autobuild Batch File - Generated on {}\n".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        batch_content += ":: Second Life Viewer Build Configuration\n\n"
        
        # Add environment variables if needed
        if self.config['installables'].get('creds'):
            batch_content += ":: Set credentials for private packages\n"
            if self.config['installables']['creds'] == "github":
                batch_content += "set AUTOBUILD_GITHUB_TOKEN=your_github_token_here\n"
            elif self.config['installables']['creds'] == "gitlab":
                batch_content += "set AUTOBUILD_GITLAB_TOKEN=your_gitlab_token_here\n"
            batch_content += "\n"
        
        # Generate commands based on configuration
        batch_content += self.generate_build_command()
        batch_content += self.generate_configure_command()
        batch_content += self.generate_edit_command()
        batch_content += self.generate_install_command()
        batch_content += self.generate_installables_command()
        batch_content += self.generate_manifest_command()
        batch_content += self.generate_package_command()
        batch_content += self.generate_print_command()
        batch_content += self.generate_source_environment_command()
        batch_content += self.generate_uninstall_command()
        batch_content += self.generate_upload_command()
        
        # Add pause at the end to keep window open
        batch_content += "\npause"
        
        # Show preview
        self.preview_text.delete(1.0, tk.END)
        self.preview_text.insert(tk.END, batch_content)
        
        # Ask to save file
        if messagebox.askyesno("Save Batch File", "Would you like to save the batch file?"):
            filename = filedialog.asksaveasfilename(
                defaultextension=".bat",
                filetypes=[("Batch files", "*.bat"), ("All files", "*.*")],
                initialfile="build_viewer.bat"
            )
            if filename:
                try:
                    with open(filename, 'w') as f:
                        f.write(batch_content)
                    messagebox.showinfo("Success", "Batch file saved successfully!")
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to save batch file: {str(e)}")
    
    def generate_build_command(self):
        cmd = ":: Build command\n"
        cmd += "autobuild build"
        
        # Add standard options
        if self.config['build']['debug']:
            cmd += " --debug"
        if self.config['build']['dry_run']:
            cmd += " --dry-run"
        if self.config['build']['verbose']:
            cmd += " --verbose"
        if self.config['build']['quiet']:
            cmd += " --quiet"
        
        # Add command-specific options
        if self.config['build']['all_configs']:
            cmd += " --all"
        if self.config['build']['configuration']:
            cmd += f" --configuration {self.config['build']['configuration']}"
        if self.config['build']['no_configure']:
            cmd += " --no-configure"
        if self.config['build']['build_id']:
            cmd += f" --id {self.config['build']['build_id']}"
        if self.config['build']['address_size']:
            cmd += f" --address-size {self.config['build']['address_size']}"
        if self.config['build']['additional_options']:
            cmd += f" -- {self.config['build']['additional_options']}"
        
        return cmd + "\n\n"
    
    def generate_configure_command(self):
        cmd = ":: Configure command\n"
        cmd += "autobuild configure"
        
        # Add standard options
        if self.config['configure']['debug']:
            cmd += " --debug"
        if self.config['configure']['dry_run']:
            cmd += " --dry-run"
        if self.config['configure']['verbose']:
            cmd += " --verbose"
        if self.config['configure']['quiet']:
            cmd += " --quiet"
        
        # Add command-specific options
        if self.config['configure']['all_configs']:
            cmd += " --all"
        if self.config['configure']['configuration']:
            cmd += f" --configuration {self.config['configure']['configuration']}"
        if self.config['configure']['address_size']:
            cmd += f" --address-size {self.config['configure']['address_size']}"
        if self.config['configure']['additional_options']:
            cmd += f" -- {self.config['configure']['additional_options']}"
        
        return cmd + "\n\n"
    
    def generate_edit_command(self):
        cmd = ":: Edit command\n"
        cmd += f"autobuild edit {self.config['edit']['subcommand']}"
        
        # Add standard options
        if self.config['edit']['debug']:
            cmd += " --debug"
        if self.config['edit']['dry_run']:
            cmd += " --dry-run"
        if self.config['edit']['verbose']:
            cmd += " --verbose"
        if self.config['edit']['quiet']:
            cmd += " --quiet"
        
        # Add command-specific options
        if self.config['edit']['config_file']:
            cmd += f" --config-file {self.config['edit']['config_file']}"
        if self.config['edit']['delete']:
            cmd += " --delete"
        
        # Add subcommand-specific options
        if self.config['edit']['subcommand'] == "build" and self.config['edit']['build_command']:
            cmd += f" {self.config['edit']['build_command']}"
        elif self.config['edit']['subcommand'] == "configure" and self.config['edit']['configure_command']:
            cmd += f" {self.config['edit']['configure_command']}"
        elif self.config['edit']['subcommand'] == "package" and self.config['edit']['package_name']:
            cmd += f" {self.config['edit']['package_name']}"
        elif self.config['edit']['subcommand'] == "platform" and self.config['edit']['platform_name']:
            cmd += f" {self.config['edit']['platform_name']}"
        
        return cmd + "\n\n"
    
    def generate_install_command(self):
        cmd = ":: Install command\n"
        cmd += "autobuild install"
        
        # Add standard options
        if self.config['install']['debug']:
            cmd += " --debug"
        if self.config['install']['dry_run']:
            cmd += " --dry-run"
        if self.config['install']['verbose']:
            cmd += " --verbose"
        if self.config['install']['quiet']:
            cmd += " --quiet"
        
        # Add command-specific options
        if self.config['install']['config_file']:
            cmd += f" --config-file {self.config['install']['config_file']}"
        if self.config['install']['install_dir']:
            cmd += f" --install-dir {self.config['install']['install_dir']}"
        if self.config['install']['manifest_file']:
            cmd += f" --installed-manifest {self.config['install']['manifest_file']}"
        if self.config['install']['export_manifest']:
            cmd += " --export-manifest"
        if self.config['install']['list']:
            cmd += " --list"
        if self.config['install']['list_installed']:
            cmd += " --list-installed"
        if self.config['install']['list_licenses']:
            cmd += " --list-licenses"
        if self.config['install']['platform']:
            cmd += f" --platform {self.config['install']['platform']}"
        
        # Add packages
        if self.config['install']['packages']:
            cmd += " " + " ".join(self.config['install']['packages'])
        
        return cmd + "\n\n"
    
    def generate_installables_command(self):
        cmd = ":: Installables command\n"
        cmd += f"autobuild installables {self.config['installables']['command']}"
        
        # Add standard options
        if self.config['installables']['debug']:
            cmd += " --debug"
        if self.config['installables']['dry_run']:
            cmd += " --dry-run"
        if self.config['installables']['verbose']:
            cmd += " --verbose"
        if self.config['installables']['quiet']:
            cmd += " --quiet"
        
        # Add command-specific options
        if self.config['installables']['config_file']:
            cmd += f" --config-file {self.config['installables']['config_file']}"
        if self.config['installables']['archive']:
            cmd += f" --archive {self.config['installables']['archive']}"
        
        # Add package name and attributes
        if self.config['installables']['pkg_name']:
            cmd += f" {self.config['installables']['pkg_name']}"
            attrs = []
            if self.config['installables']['creds']:
                attrs.append(f"creds={self.config['installables']['creds']}")
            if self.config['installables']['url']:
                attrs.append(f"url={self.config['installables']['url']}")
            if self.config['installables']['hash']:
                attrs.append(f"hash={self.config['installables']['hash']}")
            if self.config['installables']['hash_alg']:
                attrs.append(f"hash_algorithm={self.config['installables']['hash_alg']}")
            
            if attrs:
                cmd += " " + " ".join(attrs)
        
        return cmd + "\n\n"
    
    def generate_manifest_command(self):
        cmd = ":: Manifest command\n"
        cmd += f"autobuild manifest {self.config['manifest']['command']}"
        
        # Add standard options
        if self.config['manifest']['debug']:
            cmd += " --debug"
        if self.config['manifest']['dry_run']:
            cmd += " --dry-run"
        if self.config['manifest']['verbose']:
            cmd += " --verbose"
        if self.config['manifest']['quiet']:
            cmd += " --quiet"
        
        # Add command-specific options
        if self.config['manifest']['config_file']:
            cmd += f" --config-file {self.config['manifest']['config_file']}"
        if self.config['manifest']['platform']:
            cmd += f" --platform {self.config['manifest']['platform']}"
        
        # Add patterns for add command
        if self.config['manifest']['command'] == "add" and self.config['manifest']['patterns']:
            cmd += " " + " ".join(self.config['manifest']['patterns'])
        
        return cmd + "\n\n"
    
    def generate_package_command(self):
        cmd = ":: Package command\n"
        cmd += "autobuild package"
        
        # Add standard options
        if self.config['package']['debug']:
            cmd += " --debug"
        if self.config['package']['dry_run']:
            cmd += " --dry-run"
        if self.config['package']['verbose']:
            cmd += " --verbose"
        if self.config['package']['quiet']:
            cmd += " --quiet"
        
        # Add command-specific options
        if self.config['package']['config_file']:
            cmd += f" --config-file {self.config['package']['config_file']}"
        if self.config['package']['archive_name']:
            cmd += f" --archive-name {self.config['package']['archive_name']}"
        if self.config['package']['platform']:
            cmd += f" --platform {self.config['package']['platform']}"
        
        return cmd + "\n\n"
    
    def generate_print_command(self):
        cmd = ":: Print command\n"
        cmd += "autobuild print"
        
        # Add standard options
        if self.config['print']['debug']:
            cmd += " --debug"
        if self.config['print']['dry_run']:
            cmd += " --dry-run"
        if self.config['print']['verbose']:
            cmd += " --verbose"
        if self.config['print']['quiet']:
            cmd += " --quiet"
        
        # Add command-specific options
        if self.config['print']['config_file']:
            cmd += f" --config-file {self.config['print']['config_file']}"
        if self.config['print']['json']:
            cmd += " --json"
        
        return cmd + "\n\n"
    
    def generate_source_environment_command(self):
        cmd = ":: Source Environment command\n"
        cmd += "autobuild source_environment"
        
        # Add standard options
        if self.config['source_environment']['debug']:
            cmd += " --debug"
        if self.config['source_environment']['dry_run']:
            cmd += " --dry-run"
        if self.config['source_environment']['verbose']:
            cmd += " --verbose"
        if self.config['source_environment']['quiet']:
            cmd += " --quiet"
        
        # Add command-specific options
        if self.config['source_environment']['vars_file']:
            cmd += f" {self.config['source_environment']['vars_file']}"
        
        return cmd + "\n\n"
    
    def generate_uninstall_command(self):
        cmd = ":: Uninstall command\n"
        cmd += "autobuild uninstall"
        
        # Add standard options
        if self.config['uninstall']['debug']:
            cmd += " --debug"
        if self.config['uninstall']['dry_run']:
            cmd += " --dry-run"
        if self.config['uninstall']['verbose']:
            cmd += " --verbose"
        if self.config['uninstall']['quiet']:
            cmd += " --quiet"
        
        # Add command-specific options
        if self.config['uninstall']['config_file']:
            cmd += f" --config-file {self.config['uninstall']['config_file']}"
        if self.config['uninstall']['install_dir']:
            cmd += f" --install-dir {self.config['uninstall']['install_dir']}"
        if self.config['uninstall']['manifest_file']:
            cmd += f" --installed-manifest {self.config['uninstall']['manifest_file']}"
        
        # Add packages
        if self.config['uninstall']['packages']:
            cmd += " " + " ".join(self.config['uninstall']['packages'])
        
        return cmd + "\n\n"
    
    def generate_upload_command(self):
        cmd = ":: Upload command\n"
        cmd += f"autobuild upload {self.config['upload']['archive']}"
        
        # Add standard options
        if self.config['upload']['debug']:
            cmd += " --debug"
        if self.config['upload']['dry_run']:
            cmd += " --dry-run"
        if self.config['upload']['verbose']:
            cmd += " --verbose"
        if self.config['upload']['quiet']:
            cmd += " --quiet"
        
        # Add command-specific options
        if self.config['upload']['to_s3']:
            cmd += " --upload-to-s3"
        if self.config['upload']['credentials']:
            cmd += f" --credentials {self.config['upload']['credentials']}"
        
        return cmd + "\n\n"

if __name__ == "__main__":
    root = tk.Tk()
    app = AutobuildGUI(root)
    root.mainloop()
{
  description = "Python dev shell";

  inputs = {
    nixpkgs.url = "nixpkgs/nixos-unstable";
  };

  outputs = { nixpkgs, ... }:
  let
    system = "x86_64-linux";
    pkgs = nixpkgs.legacyPackages.${system};

  in {
    devShells.${system}.default = pkgs.mkShell {
      name = "python-uv-dev-shell";

      packages = with pkgs; [
        python314
        uv
        stdenv.cc.cc
        mypy
      ];

      env.LD_LIBRARY_PATH = pkgs.lib.makeLibraryPath [
        pkgs.stdenv.cc.cc.lib
        pkgs.zlib
      ];

      shellHook = ''
        echo "Python environment activated."
        echo "Python: $(python --version)"
        echo "uv:     $(uv --version)"
      '';
    };
  };
}
